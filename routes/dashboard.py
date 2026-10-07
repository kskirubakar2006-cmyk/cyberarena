from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import UserSkill, Attempt

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.role == 'admin':
        # Admin has a separate dashboard
        pass 
        
    skills = UserSkill.query.filter_by(user_id=current_user.id).all()
    recent_attempts = Attempt.query.filter_by(user_id=current_user.id).order_by(Attempt.attempted_at.desc()).limit(5).all()
    
    # Simple recommendation logic (will be expanded in services)
    from services.recommendations import get_recommended_challenge
    recommended_challenge = get_recommended_challenge(current_user)

    return render_template('dashboard.html', 
                           user=current_user, 
                           skills=skills, 
                           recent_attempts=recent_attempts,
                           recommended_challenge=recommended_challenge)
