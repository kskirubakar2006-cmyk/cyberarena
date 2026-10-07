from database import UserSkill, Scenario, Attempt
from sqlalchemy.sql.expression import func

def get_recommended_challenge(user):
    # Find user's weakest skill
    weakest_skill = UserSkill.query.filter_by(user_id=user.id).order_by(UserSkill.score.asc()).first()
    
    if weakest_skill:
        category = weakest_skill.skill.name
    else:
        category = None

    # Get scenarios the user has not completed yet
    completed_attempts = Attempt.query.filter_by(user_id=user.id, is_correct=True).all()
    completed_ids = [a.scenario_id for a in completed_attempts]
    
    query = Scenario.query.filter(Scenario.id.notin_(completed_ids), Scenario.active == True)
    
    if category:
        # Try to find a scenario in the weakest category
        cat_query = query.filter_by(category=category)
        
        # Adaptive difficulty
        if weakest_skill.score >= 80:
            scenario = cat_query.filter(Scenario.difficulty.in_(['Medium', 'Hard'])).order_by(func.random()).first()
        elif weakest_skill.score >= 50:
            scenario = cat_query.filter_by(difficulty='Medium').order_by(func.random()).first()
        else:
            scenario = cat_query.filter_by(difficulty='Easy').order_by(func.random()).first()
            
        if scenario:
            return scenario
            
    # Fallback to any random uncompleted scenario
    return query.order_by(func.random()).first()
