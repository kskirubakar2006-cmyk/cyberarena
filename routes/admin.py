import logging

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db, User, Scenario, Attempt, Option, Skill
from functools import wraps

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    users_count = User.query.filter_by(role='student').count()
    scenarios_count = Scenario.query.count()
    attempts_count = Attempt.query.count()
    
    return render_template('admin_dashboard.html', 
                           users_count=users_count, 
                           scenarios_count=scenarios_count,
                           attempts_count=attempts_count)

@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.filter_by(role='student').all()
    return render_template('admin_users.html', users=all_users)

@admin_bp.route('/scenarios')
@admin_required
def scenarios():
    all_scenarios = Scenario.query.all()
    return render_template('admin_scenarios.html', scenarios=all_scenarios)

@admin_bp.route('/scenarios/new', methods=['GET', 'POST'])
@admin_required
def create_scenario():
    categories = [skill.name for skill in Skill.query.order_by(Skill.name).all()]
    difficulties = ['Easy', 'Medium', 'Hard']
    form_data = request.form if request.method == 'POST' else None

    if request.method == 'POST':
        required_fields = {
            'title': 'Title',
            'description': 'Description',
            'scenario_text': 'Scenario question',
            'category': 'Category',
            'difficulty': 'Difficulty',
            'threat_type': 'Threat type',
            'explanation': 'Explanation',
            'security_tip': 'Security tip'
        }
        errors = [f'{label} is required.' for field, label in required_fields.items()
                  if not request.form.get(field, '').strip()]

        category = request.form.get('category', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        if category not in categories:
            errors.append('Select a valid category.')
        if difficulty not in difficulties:
            errors.append('Select a valid difficulty.')

        try:
            xp_reward = int(request.form.get('xp_reward', ''))
            if xp_reward < 0:
                errors.append('XP reward must be zero or greater.')
        except (TypeError, ValueError):
            xp_reward = 0
            errors.append('XP reward must be a whole number.')

        option_texts = request.form.getlist('option_text')
        option_explanations = request.form.getlist('option_explanation')
        if len(option_texts) < 2:
            errors.append('At least two answer options are required.')
        if any(not option_text.strip() for option_text in option_texts):
            errors.append('Every answer option must have text.')

        correct_option = request.form.get('correct_option', '')
        try:
            correct_index = int(correct_option)
            if correct_index < 0 or correct_index >= len(option_texts):
                raise ValueError
        except (TypeError, ValueError):
            correct_index = -1
            errors.append('Select exactly one correct answer.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'admin_scenario_form.html',
                categories=categories,
                difficulties=difficulties,
                form_data=form_data
            ), 400

        scenario = Scenario(
            title=request.form['title'].strip(),
            description=request.form['description'].strip(),
            scenario_text=request.form['scenario_text'].strip(),
            category=category,
            difficulty=difficulty,
            threat_type=request.form['threat_type'].strip(),
            explanation=request.form['explanation'].strip(),
            security_tip=request.form['security_tip'].strip(),
            xp_reward=xp_reward,
            active='active' in request.form
        )

        try:
            for index, option_text in enumerate(option_texts):
                explanation = option_explanations[index].strip() if index < len(option_explanations) else ''
                scenario.options.append(Option(
                    option_text=option_text.strip(),
                    is_correct=index == correct_index,
                    explanation=explanation or None
                ))
            db.session.add(scenario)
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception('Scenario creation failed for admin user %s', current_user.id)
            flash('The scenario could not be saved. No changes were committed; check the application log for details.', 'danger')
            return render_template(
                'admin_scenario_form.html',
                categories=categories,
                difficulties=difficulties,
                form_data=form_data
            ), 500

        flash('Scenario created successfully.', 'success')
        return redirect(url_for('admin.scenarios'))

    return render_template(
        'admin_scenario_form.html',
        categories=categories,
        difficulties=difficulties,
        form_data=form_data
    )
