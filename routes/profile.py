from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import UserSkill, UserBadge, Attempt, Scenario

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def index():
    user_skills = UserSkill.query.filter_by(user_id=current_user.id).all()
    user_badges = UserBadge.query.filter_by(user_id=current_user.id).all()
    
    # Get challenge history
    attempts = Attempt.query.filter_by(user_id=current_user.id).order_by(Attempt.attempted_at.desc()).limit(10).all()
    
    return render_template('profile.html', 
                           user=current_user, 
                           skills=user_skills, 
                           badges=user_badges, 
                           attempts=attempts)
