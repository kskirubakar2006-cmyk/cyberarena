import logging

from sqlalchemy import inspect

from app import create_app
from database import db, User, Scenario, Option, Attempt, Skill, UserSkill, Badge, UserBadge


logger = logging.getLogger(__name__)

DEMO_USERS = (
    {
        'name': 'CyberArena Admin',
        'email': 'admin@cyberarena.com',
        'password': 'admin123',
        'role': 'admin',
    },
    {
        'name': 'Arun Kumar',
        'email': 'arun@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 450,
        'level': 4,
        'streak': 5,
    },
    {
        'name': 'Priya Sharma',
        'email': 'priya@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 300,
        'level': 3,
        'streak': 3,
    },
    {
        'name': 'Rahul Kumar',
        'email': 'rahul@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 650,
        'level': 6,
        'streak': 8,
    },
    {
        'name': 'Sneha Raj',
        'email': 'sneha@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 200,
        'level': 2,
        'streak': 2,
    },
    {
        'name': 'Karthik M',
        'email': 'karthik@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 800,
        'level': 8,
        'streak': 10,
    },
    {
        'name': 'Divya S',
        'email': 'divya@cyberarena.com',
        'password': 'student123',
        'role': 'student',
        'xp': 500,
        'level': 5,
        'streak': 6,
    },
)

SCENARIOS = (
    {
        'title': 'Suspicious Bank Email',
        'category': 'Phishing',
        'difficulty': 'Easy',
        'description': 'A bank email pressures you to verify your account through an urgent link.',
        'scenario_text': "You receive an email claiming to be from your bank. It asks you to urgently click a link and verify your account because it will otherwise be suspended. What should you do?",
        'threat_type': 'Phishing and credential theft',
        'explanation': 'Unexpected urgent requests can lead to a fake sign-in page. Verify through contact details you already know are official.',
        'security_tip': 'Do not use links or phone numbers in an unexpected message to verify its claims.',
        'xp_reward': 50,
        'options': (
            ('Click the link and verify immediately', False, 'Urgency is being used to push you into a risky action.'),
            ('Reply to the email asking whether it is legitimate', False, 'A reply does not verify the sender and may confirm your address is active.'),
            ("Avoid the link and verify the message through the bank's official website or phone number", True, 'Use an independently located official channel to check the message.'),
            ('Forward the email to friends', False, 'Forwarding could expose others to the same malicious link.'),
        ),
    },
    {
        'title': 'Weak Password',
        'category': 'Password Security',
        'difficulty': 'Easy',
        'description': 'Choose a password that is difficult to guess and safe to use for one account.',
        'scenario_text': 'Which password is the strongest choice?',
        'threat_type': 'Weak or guessable password',
        'explanation': 'A long, unique passphrase is harder to guess and limits the impact if another service is breached.',
        'security_tip': 'Use a password manager to create and store unique passwords.',
        'xp_reward': 50,
        'options': (
            ('password123', False, 'This common pattern is easy to guess.'),
            ('john2004', False, 'Names and dates can often be guessed from public information.'),
            ('P@ssword', False, 'A predictable word with a simple substitution is still weak.'),
            ('A long unique passphrase that is not reused elsewhere', True, 'Length and uniqueness improve resistance to guessing and credential reuse.'),
        ),
    },
    {
        'title': 'Public Wi-Fi Login',
        'category': 'Network Security',
        'difficulty': 'Medium',
        'description': 'Protect an important account while connected to airport public Wi-Fi.',
        'scenario_text': 'You are using public Wi-Fi at an airport and need to access an important account. What is the safest approach?',
        'threat_type': 'Untrusted public network',
        'explanation': 'A trusted VPN can protect traffic on an untrusted network, and HTTPS protects the connection to the service.',
        'security_tip': 'Avoid sensitive tasks on untrusted networks when possible; use a trusted VPN and verify HTTPS.',
        'xp_reward': 75,
        'options': (
            ('Use the account normally without precautions', False, 'Public networks can be untrusted or impersonated.'),
            ('Use a trusted VPN and HTTPS-enabled service', True, 'A trusted VPN and HTTPS add protection to the connection.'),
            ('Disable all security software', False, 'Disabling protection increases risk.'),
            ('Share your password with a friend', False, 'Passwords should not be shared.'),
        ),
    },
    {
        'title': 'Unknown USB Drive',
        'category': 'Malware',
        'difficulty': 'Easy',
        'description': 'An unidentified USB drive is found in a college laboratory.',
        'scenario_text': 'You find an unknown USB drive in your college laboratory. What should you do?',
        'threat_type': 'Removable-media malware',
        'explanation': 'Unknown removable media can contain malware or attempt to exploit a connected device.',
        'security_tip': 'Give found media to the responsible administrator; do not connect it to a computer.',
        'xp_reward': 50,
        'options': (
            ('Plug it into your laptop immediately', False, 'Connecting unknown media can expose your device.'),
            ('Give it to a friend to test', False, 'This transfers the risk to another person.'),
            ('Connect it to a computer containing important files', False, 'This could expose sensitive data or systems.'),
            ('Avoid connecting it and report it to the responsible administrator', True, 'Reporting it avoids exposing devices and lets staff handle it safely.'),
        ),
    },
    {
        'title': 'Fake Technical Support',
        'category': 'Social Engineering',
        'difficulty': 'Medium',
        'description': 'A caller claiming to be support asks for your account password.',
        'scenario_text': 'Someone calls claiming to be technical support and asks for your password to fix a security issue. What should you do?',
        'threat_type': 'Impersonation and credential theft',
        'explanation': 'Legitimate support should not need your password. Independently contact the organization using an official channel.',
        'security_tip': 'Never disclose a password to a caller; end the call and contact support through a known number.',
        'xp_reward': 75,
        'options': (
            ('Give them the password', False, 'This gives an unverified caller account access.'),
            ('Ask them to send their employee ID and then give the password', False, 'An ID supplied by the caller is not independent verification.'),
            ('Refuse to provide the password and contact official support independently', True, 'Independent contact verifies the request without disclosing credentials.'),
            ('Give them a temporary password', False, 'A temporary password can still grant account access.'),
        ),
    },
    {
        'title': 'Software Updates',
        'category': 'Cyber Hygiene',
        'difficulty': 'Easy',
        'description': 'Understand why applying software updates matters for security.',
        'scenario_text': 'Why are software updates important for cybersecurity?',
        'threat_type': 'Unpatched software vulnerabilities',
        'explanation': 'Updates commonly fix security vulnerabilities and bugs that could otherwise be exploited.',
        'security_tip': 'Install updates from the operating system or application vendor promptly.',
        'xp_reward': 50,
        'options': (
            ('They only change the appearance of the application', False, 'Updates often include security fixes, not just visual changes.'),
            ('They can fix security vulnerabilities and bugs', True, 'Security updates reduce exposure to known vulnerabilities.'),
            ('They always make the computer slower', False, 'This is not the purpose of updates.'),
            ('They remove all personal files', False, 'Updates are not intended to remove personal files.'),
        ),
    },
    {
        'title': 'Two-Factor Authentication',
        'category': 'Authentication',
        'difficulty': 'Easy',
        'description': 'Identify the purpose of multi-factor authentication.',
        'scenario_text': 'What is the main purpose of multi-factor authentication?',
        'threat_type': 'Account takeover risk',
        'explanation': 'MFA adds another verification factor, helping protect an account if a password is exposed.',
        'security_tip': 'Enable MFA, preferably with a passkey or authenticator method supported by the service.',
        'xp_reward': 50,
        'options': (
            ('To make passwords shorter', False, 'MFA adds verification; it does not change password length.'),
            ('To provide an additional verification factor', True, 'A second factor adds another check during sign-in.'),
            ('To remove the need for usernames', False, 'MFA does not replace the account identifier.'),
            ('To disable account security', False, 'MFA strengthens account security.'),
        ),
    },
    {
        'title': 'Malicious Attachment',
        'category': 'Email Security',
        'difficulty': 'Medium',
        'description': 'An unexpected email contains an executable attachment.',
        'scenario_text': 'You receive an unexpected email containing an executable attachment. What should you do?',
        'threat_type': 'Malicious email attachment',
        'explanation': 'Unexpected executable files can install malware. Verify the message with the sender through a trusted channel.',
        'security_tip': 'Do not open unexpected attachments; report suspicious email using your organization’s process.',
        'xp_reward': 75,
        'options': (
            ('Open it immediately', False, 'Opening an unknown executable can run malicious code.'),
            ('Download it and scan it later', False, 'Downloading still introduces an untrusted file to your device.'),
            ('Avoid opening it and verify the sender through another trusted channel', True, 'Independent verification helps establish whether the attachment is expected.'),
            ('Forward it to another person', False, 'Forwarding may spread the malicious attachment.'),
        ),
    },
    {
        'title': 'SQL Injection',
        'category': 'Web Security',
        'difficulty': 'Hard',
        'description': 'Choose an application design practice that prevents SQL injection.',
        'scenario_text': 'Which practice helps protect a web application from SQL injection?',
        'threat_type': 'SQL injection',
        'explanation': 'Parameterized queries keep user input separate from SQL code so input is not interpreted as query structure.',
        'security_tip': 'Use parameterized queries or safe ORM APIs and validate input for its intended use.',
        'xp_reward': 100,
        'options': (
            ('Using parameterized queries', True, 'Parameters separate data from executable SQL syntax.'),
            ('Removing all passwords', False, 'This does not prevent SQL injection.'),
            ('Disabling database backups', False, 'Backups do not prevent injection vulnerabilities.'),
            ('Increasing the screen brightness', False, 'Display brightness has no effect on query security.'),
        ),
    },
    {
        'title': 'Data Privacy',
        'category': 'Data Privacy',
        'difficulty': 'Medium',
        'description': 'Select a practice that limits exposure of sensitive personal information.',
        'scenario_text': 'Which practice helps protect sensitive personal information?',
        'threat_type': 'Unnecessary data exposure',
        'explanation': 'Limiting access to sensitive data reduces the number of people and systems that could expose it.',
        'security_tip': 'Collect only necessary personal data and grant access on a need-to-know basis.',
        'xp_reward': 75,
        'options': (
            ('Sharing sensitive information publicly', False, 'Public sharing exposes information to an unrestricted audience.'),
            ('Collecting and storing unnecessary personal data', False, 'Unneeded data increases the impact of a breach.'),
            ('Limiting access to sensitive data', True, 'Restricting access reduces unnecessary exposure.'),
            ('Posting passwords in documents', False, 'Passwords should not be stored in shared documents.'),
        ),
    },
    {
        'title': 'HTTPS',
        'category': 'Web Security',
        'difficulty': 'Easy',
        'description': 'Recognize the security property provided by HTTPS.',
        'scenario_text': 'What does HTTPS primarily provide for communication between a browser and website?',
        'threat_type': 'Insecure web communication',
        'explanation': 'HTTPS uses TLS to encrypt communication and authenticate the website endpoint.',
        'security_tip': 'Check that the address is correct and HTTPS is used, while remembering that HTTPS alone does not prove a site is trustworthy.',
        'xp_reward': 50,
        'options': (
            ('Encrypted communication', True, 'TLS encrypts data in transit between the browser and website.'),
            ('Free internet access', False, 'HTTPS does not provide internet access.'),
            ('Faster CPU performance', False, 'HTTPS does not change the computer’s CPU performance.'),
            ('Unlimited storage', False, 'HTTPS does not provide storage.'),
        ),
    },
    {
        'title': 'Password Reuse',
        'category': 'Password Security',
        'difficulty': 'Medium',
        'description': 'Understand how reusing credentials can spread the impact of a breach.',
        'scenario_text': 'Why is reusing the same password across multiple websites risky?',
        'threat_type': 'Credential stuffing',
        'explanation': 'Attackers may try exposed credentials on other services, potentially compromising multiple accounts.',
        'security_tip': 'Use a different strong password for every account.',
        'xp_reward': 75,
        'options': (
            ('It makes websites load slower', False, 'Password reuse is an account-security risk, not a performance issue.'),
            ('A compromised password can potentially expose multiple accounts', True, 'Attackers commonly test leaked passwords on other services.'),
            ('It increases monitor brightness', False, 'Display brightness is unrelated to credential safety.'),
            ('It prevents software updates', False, 'Password reuse does not affect software updates.'),
        ),
    },
    {
        'title': 'Ransomware',
        'category': 'Malware',
        'difficulty': 'Hard',
        'description': 'Identify a common behavior associated with ransomware.',
        'scenario_text': 'What is a common characteristic of ransomware?',
        'threat_type': 'Ransomware',
        'explanation': 'Ransomware commonly encrypts or otherwise blocks access to files and demands payment.',
        'security_tip': 'Maintain tested offline or protected backups and report suspected ransomware immediately.',
        'xp_reward': 100,
        'options': (
            ('It encrypts files and demands payment', True, 'This is a common ransomware behavior.'),
            ('It improves computer performance', False, 'Ransomware is malicious and does not improve performance.'),
            ('It creates stronger passwords automatically', False, 'Ransomware does not improve account passwords.'),
            ('It blocks advertisements only', False, 'Ad blocking alone is not ransomware behavior.'),
        ),
    },
    {
        'title': 'Shoulder Surfing',
        'category': 'Social Engineering',
        'difficulty': 'Medium',
        'description': 'Recognize the risk of someone observing a password entered in public.',
        'scenario_text': 'Someone is standing close behind you while you enter your banking password in a public place. What attack technique could this represent?',
        'threat_type': 'Shoulder surfing',
        'explanation': 'Shoulder surfing is the observation of sensitive information, such as credentials, over someone’s shoulder.',
        'security_tip': 'Shield the keypad or screen and avoid entering credentials when others can observe.',
        'xp_reward': 75,
        'options': (
            ('Shoulder surfing', True, 'The person may be observing your credentials as you enter them.'),
            ('SQL injection', False, 'SQL injection targets application queries, not a person watching a screen.'),
            ('DDoS', False, 'A distributed denial-of-service attack disrupts service availability.'),
            ('Encryption', False, 'Encryption protects data; it is not the described observation technique.'),
        ),
    },
    {
        'title': 'Account Lockout',
        'category': 'Authentication',
        'difficulty': 'Hard',
        'description': 'Understand how lockout policies can slow repeated login guessing.',
        'scenario_text': 'Why can account lockout policies help protect user accounts?',
        'threat_type': 'Repeated password guessing',
        'explanation': 'Rate limits and carefully designed lockout policies can slow repeated guesses against an account.',
        'security_tip': 'Use rate limiting and alerting alongside MFA; avoid policies that let attackers easily lock out other users.',
        'xp_reward': 100,
        'options': (
            ('They limit repeated failed login attempts', True, 'Limiting attempts slows online password guessing.'),
            ('They remove all authentication', False, 'Authentication remains necessary to protect accounts.'),
            ('They make passwords visible', False, 'Passwords should never be displayed in this way.'),
            ('They disable encryption', False, 'Lockout policies do not disable encryption.'),
        ),
    },
)

SKILL_NAMES = tuple(dict.fromkeys(scenario['category'] for scenario in SCENARIOS))

BADGES = (
    ('First Step', 'Complete a first cybersecurity scenario.', 'fas fa-shoe-prints', 'first_attempt'),
    ('Phishing Hunter', 'Correctly identify five phishing scenarios.', 'fas fa-fish', '5_phishing'),
    ('Cyber Learner', 'Complete five cybersecurity scenarios.', 'fas fa-book-open', '5_attempts'),
    ('Security Expert', 'Answer ten scenarios correctly.', 'fas fa-shield-alt', '10_correct'),
    ('5 Day Streak', 'Reach a five-day learning streak.', 'fas fa-fire', '5_streak'),
    ('10 Day Streak', 'Reach a ten-day learning streak.', 'fas fa-fire-alt', '10_streak'),
    ('Scam Detector', 'Correctly identify five digital payment scams.', 'fas fa-money-bill-wave', '5_scam'),
    ('Security Streak', 'Reach a seven-day learning streak.', 'fas fa-calendar-check', '7_streak'),
)

ATTEMPT_PLANS = {
    'arun@cyberarena.com': (8, 6),
    'priya@cyberarena.com': (6, 4),
    'rahul@cyberarena.com': (12, 10),
    'sneha@cyberarena.com': (5, 3),
    'karthik@cyberarena.com': (15, 13),
    'divya@cyberarena.com': (9, 7),
}


def validate_demo_content():
    titles = [scenario['title'] for scenario in SCENARIOS]
    if len(titles) < 15 or len(titles) != len(set(titles)):
        raise ValueError('Demo scenario titles must contain at least 15 unique entries.')

    for scenario in SCENARIOS:
        options = scenario['options']
        if len(options) not in (3, 4) or sum(bool(option[1]) for option in options) != 1:
            raise ValueError(f"Scenario {scenario['title']!r} must have 3 or 4 options and exactly one correct answer.")
        if scenario['difficulty'] not in {'Easy', 'Medium', 'Hard'}:
            raise ValueError(f"Scenario {scenario['title']!r} has an invalid difficulty.")
        if scenario['xp_reward'] < 0:
            raise ValueError(f"Scenario {scenario['title']!r} has an invalid XP reward.")


def add_missing_demo_data():
    validate_demo_content()
    app = create_app()
    created = {
        'users': 0,
        'scenarios': 0,
        'options': 0,
        'skills': 0,
        'attempts': 0,
        'badges': 0,
        'user_badges': 0,
        'user_skills': 0,
    }

    with app.app_context():
        required_tables = {
            'users', 'scenarios', 'options', 'attempts', 'skills',
            'user_skills', 'badges', 'user_badges',
        }
        missing_tables = required_tables - set(inspect(db.engine).get_table_names())
        if missing_tables:
            raise RuntimeError(
                'Required database tables are missing; no schema changes were made: '
                + ', '.join(sorted(missing_tables))
            )

        try:
            users_by_email = {user.email: user for user in User.query.all()}
            for user_data in DEMO_USERS:
                user = users_by_email.get(user_data['email'])
                if user is None:
                    user = User(
                        name=user_data['name'],
                        email=user_data['email'],
                        role=user_data['role'],
                    )
                    user.set_password(user_data['password'])
                    if user_data['role'] == 'student':
                        user.xp = user_data['xp']
                        user.total_score = user_data['xp']
                        user.level = user_data['level']
                        user.streak = user_data['streak']
                    db.session.add(user)
                    users_by_email[user.email] = user
                    created['users'] += 1

            skills_by_name = {skill.name: skill for skill in Skill.query.all()}
            for skill_name in SKILL_NAMES:
                if skill_name not in skills_by_name:
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                    skills_by_name[skill_name] = skill
                    created['skills'] += 1

            badges_by_name = {badge.name: badge for badge in Badge.query.all()}
            for name, description, icon, requirement in BADGES:
                if name not in badges_by_name:
                    badge = Badge(
                        name=name,
                        description=description,
                        icon=icon,
                        requirement=requirement,
                    )
                    db.session.add(badge)
                    badges_by_name[name] = badge
                    created['badges'] += 1

            scenarios_by_title = {scenario.title: scenario for scenario in Scenario.query.all()}
            for scenario_data in SCENARIOS:
                if scenario_data['title'] in scenarios_by_title:
                    continue

                scenario = Scenario(
                    title=scenario_data['title'],
                    category=scenario_data['category'],
                    difficulty=scenario_data['difficulty'],
                    description=scenario_data['description'],
                    scenario_text=scenario_data['scenario_text'],
                    threat_type=scenario_data['threat_type'],
                    explanation=scenario_data['explanation'],
                    security_tip=scenario_data['security_tip'],
                    xp_reward=scenario_data['xp_reward'],
                    active=True,
                )
                for option_text, is_correct, explanation in scenario_data['options']:
                    scenario.options.append(Option(
                        option_text=option_text,
                        is_correct=is_correct,
                        explanation=explanation,
                    ))
                    created['options'] += 1
                db.session.add(scenario)
                scenarios_by_title[scenario.title] = scenario
                created['scenarios'] += 1

            db.session.flush()

            for email, (attempt_count, correct_count) in ATTEMPT_PLANS.items():
                user = users_by_email[email]
                for index in range(attempt_count):
                    scenario_data = SCENARIOS[index]
                    scenario = scenarios_by_title[scenario_data['title']]
                    if Attempt.query.filter_by(user_id=user.id, scenario_id=scenario.id).first():
                        continue

                    should_be_correct = index < correct_count
                    selected_option = next(
                        (
                            option for option in scenario.options
                            if bool(option.is_correct) == should_be_correct
                        ),
                        None,
                    )
                    if selected_option is None:
                        logger.warning(
                            'Skipping demo attempt: scenario %s has no %s option.',
                            scenario.title,
                            'correct' if should_be_correct else 'incorrect',
                        )
                        continue

                    db.session.add(Attempt(
                        user_id=user.id,
                        scenario_id=scenario.id,
                        selected_option_id=selected_option.id,
                        is_correct=should_be_correct,
                        score=scenario.xp_reward if should_be_correct else 0,
                        response_time=24 + index * 3,
                    ))
                    created['attempts'] += 1

            db.session.flush()

            for email in ATTEMPT_PLANS:
                user = users_by_email[email]
                user_attempts = Attempt.query.filter_by(user_id=user.id).all()
                attempts_by_skill = {}
                for attempt in user_attempts:
                    scenario = scenarios_by_title.get(attempt.scenario.title, attempt.scenario)
                    counts = attempts_by_skill.setdefault(scenario.category, [0, 0])
                    counts[0] += 1
                    counts[1] += int(bool(attempt.is_correct))

                for category, (attempts, correct_attempts) in attempts_by_skill.items():
                    skill = skills_by_name.get(category)
                    if skill is None:
                        continue
                    existing_skill = UserSkill.query.filter_by(
                        user_id=user.id,
                        skill_id=skill.id,
                    ).first()
                    if existing_skill:
                        continue
                    db.session.add(UserSkill(
                        user_id=user.id,
                        skill_id=skill.id,
                        attempts=attempts,
                        correct_attempts=correct_attempts,
                        score=round(correct_attempts * 100 / attempts) if attempts else 0,
                    ))
                    created['user_skills'] += 1

            badge_assignments = {email: {'First Step', 'Cyber Learner'} for email in ATTEMPT_PLANS}
            for email, (attempt_count, correct_count) in ATTEMPT_PLANS.items():
                user_data = next(item for item in DEMO_USERS if item['email'] == email)
                if correct_count >= 10:
                    badge_assignments[email].add('Security Expert')
                if user_data['streak'] >= 5:
                    badge_assignments[email].add('5 Day Streak')
                if user_data['streak'] >= 10:
                    badge_assignments[email].add('10 Day Streak')
                if user_data['streak'] >= 7:
                    badge_assignments[email].add('Security Streak')

            for email, badge_names in badge_assignments.items():
                user = users_by_email[email]
                for badge_name in badge_names:
                    badge = badges_by_name[badge_name]
                    existing_assignment = UserBadge.query.filter_by(
                        user_id=user.id,
                        badge_id=badge.id,
                    ).first()
                    if existing_assignment:
                        continue
                    db.session.add(UserBadge(user_id=user.id, badge_id=badge.id))
                    created['user_badges'] += 1

            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception('Demo data transaction failed; all pending inserts were rolled back.')
            raise

        totals = {
            'users': User.query.count(),
            'scenarios': Scenario.query.count(),
            'options': Option.query.count(),
            'attempts': Attempt.query.count(),
            'skills': Skill.query.count(),
            'user_skills': UserSkill.query.count(),
            'badges': Badge.query.count(),
            'user_badges': UserBadge.query.count(),
        }

    print('========================================')
    print('CyberArena Demo Data')
    print(f"Users created: {created['users']}")
    print(f"Scenarios created: {created['scenarios']}")
    print(f"Options created: {created['options']}")
    print(f"Skills created: {created['skills']}")
    print(f"Attempts created: {created['attempts']}")
    print(f"User skill records created: {created['user_skills']}")
    print(f"Badges created: {created['badges']}")
    print(f"User badge assignments created: {created['user_badges']}")
    print('')
    print('Database totals:')
    for name, count in totals.items():
        print(f'  {name}: {count}')
    print('')
    print('Existing records preserved.')
    print('No tables were dropped or recreated.')
    print('Demo data successfully added.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    add_missing_demo_data()