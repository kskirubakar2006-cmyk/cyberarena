from database import db, Badge, UserBadge, Attempt, Scenario

def check_and_award_badges(user):
    badges = Badge.query.all()
    user_badges = [ub.badge_id for ub in user.badges]
    
    # Check Phishing Hunter (5 phishing scenarios correct)
    phishing_badge = next((b for b in badges if b.name == 'Phishing Hunter'), None)
    if phishing_badge and phishing_badge.id not in user_badges:
        correct_phishing = Attempt.query.join(Scenario).filter(
            Attempt.user_id == user.id,
            Attempt.is_correct == True,
            Scenario.category == 'Phishing'
        ).count()
        if correct_phishing >= 5:
            award_badge(user, phishing_badge)

    # Check Scam Detector (5 digital payment/scam scenarios correct)
    scam_badge = next((b for b in badges if b.name == 'Scam Detector'), None)
    if scam_badge and scam_badge.id not in user_badges:
        correct_scam = Attempt.query.join(Scenario).filter(
            Attempt.user_id == user.id,
            Attempt.is_correct == True,
            Scenario.category == 'Digital Payment'
        ).count()
        if correct_scam >= 5:
            award_badge(user, scam_badge)

    # Check Security Streak (7 day streak)
    streak_badge = next((b for b in badges if b.name == 'Security Streak'), None)
    if streak_badge and streak_badge.id not in user_badges:
        if user.streak >= 7:
            award_badge(user, streak_badge)

def award_badge(user, badge):
    new_ub = UserBadge(user_id=user.id, badge_id=badge.id)
    db.session.add(new_ub)
