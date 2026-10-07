import pytest
from app import create_app
from database import db, User, Scenario, Option, Skill, UserSkill, Attempt

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        
        # Setup basic data
        student = User(name="Test User", email="test@test.com")
        student.set_password("password")
        
        admin = User(name="Admin", email="admin@test.com", role="admin")
        admin.set_password("adminpass")
        
        s1 = Scenario(title="Test Scenario", category="Phishing", difficulty="Easy", description="Test", scenario_text="Test", threat_type="Test", explanation="Test", security_tip="Test")
        
        db.session.add(student)
        db.session.add(admin)
        db.session.add(s1)
        db.session.add(Skill(name='Phishing'))
        db.session.commit()
        
        o1 = Option(scenario_id=s1.id, option_text="Correct", is_correct=True)
        o2 = Option(scenario_id=s1.id, option_text="Wrong", is_correct=False)
        db.session.add_all([o1, o2])
        db.session.commit()
        
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CYBERARENA' in response.data

def test_login(client):
    response = client.post('/login', data={'email': 'test@test.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_admin_access_denied_for_student(client):
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'}, follow_redirects=True)
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert b'You do not have permission' in response.data

def test_admin_access_allowed_for_admin(client):
    client.post('/login', data={'email': 'admin@test.com', 'password': 'adminpass'}, follow_redirects=True)
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_arena_requires_login(client):
    response = client.get('/arena')
    assert response.status_code == 302 # Redirect to login

def test_correct_answer_updates_progress_and_normalizes_null_skill_counters(app, client):
    with app.app_context():
        student = User.query.filter_by(email='test@test.com').first()
        skill = Skill.query.filter_by(name='Phishing').first()
        db.session.add(UserSkill(
            user_id=student.id,
            skill_id=skill.id,
            attempts=None,
            correct_attempts=None,
            score=None
        ))
        db.session.commit()
        correct_option = Option.query.filter_by(option_text='Correct').first()
        scenario_id = correct_option.scenario_id
        option_id = correct_option.id

    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    response = client.post('/api/submit_answer', json={
        'scenario_id': scenario_id,
        'option_id': option_id,
        'response_time': 10
    })

    assert response.status_code == 200
    assert response.is_json
    assert response.json['success'] is True
    assert response.json['is_correct'] is True
    assert response.json['xp_earned'] == 120
    with app.app_context():
        student = User.query.filter_by(email='test@test.com').first()
        user_skill = UserSkill.query.one()
        assert student.xp == 120
        assert student.total_score == 120
        assert student.streak == 1
        assert user_skill.attempts == 1
        assert user_skill.correct_attempts == 1
        assert user_skill.score == 100
        assert Attempt.query.count() == 1

def test_incorrect_answer_records_attempt_without_xp_and_resets_streak(app, client):
    with app.app_context():
        student = User.query.filter_by(email='test@test.com').first()
        student.streak = 3
        db.session.commit()
        wrong_option = Option.query.filter_by(option_text='Wrong').first()
        scenario_id = wrong_option.scenario_id
        option_id = wrong_option.id

    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    response = client.post('/api/submit_answer', json={
        'scenario_id': scenario_id,
        'option_id': option_id,
        'response_time': 20
    })

    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['is_correct'] is False
    assert response.json['xp_earned'] == 0
    with app.app_context():
        db.session.expire_all()
        student = User.query.filter_by(email='test@test.com').first()
        user_skill = UserSkill.query.one()
        assert student.xp == 0
        assert student.total_score == 0
        assert student.streak == 0
        assert user_skill.attempts == 1
        assert user_skill.correct_attempts == 0
        assert user_skill.score == 0
        assert Attempt.query.count() == 1

def test_answer_rejects_missing_scenario_with_json_error(client):
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    response = client.post('/api/submit_answer', json={'scenario_id': 999, 'option_id': 1})
    assert response.status_code == 404
    assert response.json['success'] is False

def test_badge_check_failure_is_logged_without_failing_answer(app, client, monkeypatch, caplog):
    import routes.challenges as challenge_routes

    def fail_badge_check(user):
        raise RuntimeError('simulated badge storage failure')

    monkeypatch.setattr(challenge_routes, 'check_and_award_badges', fail_badge_check)
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    with app.app_context():
        correct_option = Option.query.filter_by(option_text='Correct').first()
        scenario_id = correct_option.scenario_id
        option_id = correct_option.id

    response = client.post('/api/submit_answer', json={
        'scenario_id': scenario_id,
        'option_id': option_id,
        'response_time': 20
    })

    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['is_correct'] is True
    assert 'Badge checking failed' in caplog.text
    assert 'simulated badge storage failure' in caplog.text
    with app.app_context():
        assert Attempt.query.count() == 1

def test_admin_can_create_scenario_with_options_and_it_appears_in_arena(app, client):
    with app.app_context():
        db.session.add(Skill(name='Web Safety'))
        db.session.commit()
    client.post('/login', data={'email': 'admin@test.com', 'password': 'adminpass'})
    form_response = client.get('/admin/scenarios/new')
    assert form_response.status_code == 200
    assert b'Scenario Question / Situation' in form_response.data
    assert b'Answer Options' in form_response.data

    form_data = {
        'title': 'Admin-created scenario',
        'description': 'A test description',
        'scenario_text': 'A suspicious link arrives.',
        'category': 'Web Safety',
        'difficulty': 'Medium',
        'threat_type': 'Suspicious link',
        'explanation': 'Check links before opening them.',
        'security_tip': 'Use trusted sources.',
        'xp_reward': '80',
        'active': 'on',
        'option_text': ['Open the link', 'Report the message'],
        'option_explanation': ['', 'Reporting lets the team investigate.'],
        'correct_option': '1'
    }
    response = client.post('/admin/scenarios/new', data=form_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Scenario created successfully.' in response.data
    assert b'Admin-created scenario' in response.data
    with app.app_context():
        scenario = Scenario.query.filter_by(title='Admin-created scenario').one()
        assert scenario.category == 'Web Safety'
        assert scenario.xp_reward == 80
        assert len(scenario.options) == 2
        assert sum(option.is_correct for option in scenario.options) == 1

    client.get('/logout')
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    arena_response = client.get('/arena')
    assert b'Admin-created scenario' in arena_response.data

def test_student_cannot_access_scenario_creation(client):
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    response = client.get('/admin/scenarios/new', follow_redirects=True)
    assert response.status_code == 200
    assert b'You do not have permission' in response.data

def test_admin_scenario_creation_validates_inputs_without_creating_a_row(client):
    client.post('/login', data={'email': 'admin@test.com', 'password': 'adminpass'})
    response = client.post('/admin/scenarios/new', data={
        'title': 'Invalid scenario',
        'description': 'Description',
        'scenario_text': 'Situation',
        'category': 'Unknown',
        'difficulty': 'Easy',
        'threat_type': 'Test threat',
        'explanation': 'Explanation',
        'security_tip': 'Tip',
        'xp_reward': '-1',
        'option_text': ['Only one option'],
        'correct_option': '0'
    })
    assert response.status_code == 400
    assert b'Select a valid category.' in response.data
    assert b'XP reward must be zero or greater.' in response.data
    assert b'At least two answer options are required.' in response.data
    with client.application.app_context():
        assert Scenario.query.filter_by(title='Invalid scenario').first() is None
