import logging

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from database import db, Scenario, Option, Attempt
from services.scoring import calculate_score, update_user_progression
from services.badges import check_and_award_badges

challenges_bp = Blueprint('challenges', __name__)
logger = logging.getLogger(__name__)

@challenges_bp.route('/arena')
@login_required
def arena():
    # Group scenarios by category
    scenarios = Scenario.query.filter_by(active=True).all()
    categories = {}
    for s in scenarios:
        if s.category not in categories:
            categories[s.category] = []
        categories[s.category].append(s)
        
    # Get completed scenarios for the current user
    attempts = Attempt.query.filter_by(user_id=current_user.id, is_correct=True).all()
    completed_ids = [a.scenario_id for a in attempts]
    
    return render_template('arena.html', categories=categories, completed_ids=completed_ids)

@challenges_bp.route('/challenge/<int:scenario_id>')
@login_required
def challenge(scenario_id):
    scenario = Scenario.query.get_or_404(scenario_id)
    return render_template('challenge.html', scenario=scenario)

@challenges_bp.route('/api/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(success=False, error='A JSON answer is required.'), 400

    try:
        scenario_id = int(data.get('scenario_id'))
        option_id = int(data.get('option_id'))
        response_time = int(data.get('response_time', 0))
        if scenario_id < 1 or option_id < 1 or response_time < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify(success=False, error='Scenario, option, and response time must be valid values.'), 400

    scenario = db.session.get(Scenario, scenario_id)
    if scenario is None:
        return jsonify(success=False, error='Scenario not found.'), 404

    option = Option.query.filter_by(id=option_id, scenario_id=scenario.id).first()
    if option is None:
        return jsonify(success=False, error='The selected option does not belong to this scenario.'), 400

    is_correct = bool(option.is_correct)
    score = calculate_score(scenario, option, response_time) if is_correct else 0

    try:
        attempt = Attempt(
            user_id=current_user.id,
            scenario_id=scenario.id,
            selected_option_id=option.id,
            is_correct=is_correct,
            score=score,
            response_time=response_time
        )
        db.session.add(attempt)
        update_user_progression(current_user, scenario, is_correct, score)

        try:
            with db.session.begin_nested():
                check_and_award_badges(current_user)
        except Exception:
            logger.exception('Badge checking failed for user %s after scenario %s', current_user.id, scenario.id)

        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Answer submission failed for user %s and scenario %s', current_user.id, scenario.id)
        return jsonify(success=False, error='The answer could not be recorded. No progress was saved.'), 500

    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'explanation': option.explanation or scenario.explanation,
        'security_tip': scenario.security_tip,
        'xp_earned': score,
        'threat_type': scenario.threat_type
    })
