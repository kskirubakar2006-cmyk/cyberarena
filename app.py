from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from database import db, User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from routes.challenges import challenges_bp
    app.register_blueprint(challenges_bp)
    
    from routes.leaderboard import leaderboard_bp
    app.register_blueprint(leaderboard_bp)
    
    from routes.profile import profile_bp
    app.register_blueprint(profile_bp)
    
    from routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Base routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/learn')
    def learn():
        return render_template('learn.html')

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
