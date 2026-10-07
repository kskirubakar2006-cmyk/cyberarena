from flask import Blueprint, render_template
from flask_login import login_required
from database import User

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard')
@login_required
def index():
    # Only get student users, order by XP descending
    top_users = User.query.filter_by(role='student').order_by(User.xp.desc()).limit(50).all()
    return render_template('leaderboard.html', users=top_users)
