from database import db, Skill, UserSkill
from datetime import datetime


def calculate_score(scenario, option, response_time):
    base_score = scenario.xp_reward or 0

    # Time bonus: if answered quickly (under 15 seconds)
    if response_time < 15:
        base_score += 20

    return base_score


def update_user_progression(user, scenario, is_correct, score):
    user.xp = user.xp or 0
    user.total_score = user.total_score or 0
    user.streak = user.streak or 0

    if is_correct:
        user.xp += score
        user.total_score += score
        user.streak += 1

        # Calculate new level
        if user.xp >= 4000:
            user.level = 7
        elif user.xp >= 3000:
            user.level = 6
        elif user.xp >= 2000:
            user.level = 5
        elif user.xp >= 1200:
            user.level = 4
        elif user.xp >= 700:
            user.level = 3
        elif user.xp >= 200:
            user.level = 2

    else:
        # Reset streak on failure, no XP gained
        user.streak = 0

    user.last_active = datetime.utcnow()

    # Update skills
    skill = Skill.query.filter_by(name=scenario.category).first()

    if skill:
        user_skill = UserSkill.query.filter_by(
            user_id=user.id,
            skill_id=skill.id
        ).first()

        if not user_skill:
            user_skill = UserSkill(
                user_id=user.id,
                skill_id=skill.id,
                attempts=0,
                correct_attempts=0,
                score=0
            )
            db.session.add(user_skill)
            db.session.flush()

        # Make sure NULL values don't cause None + 1 errors
        user_skill.attempts = user_skill.attempts or 0
        user_skill.correct_attempts = user_skill.correct_attempts or 0

        # Record this attempt
        user_skill.attempts += 1

        if is_correct:
            user_skill.correct_attempts += 1

        # Calculate percentage score safely
        if user_skill.attempts > 0:
            user_skill.score = int(
                (user_skill.correct_attempts / user_skill.attempts) * 100
            )
        else:
            user_skill.score = 0

