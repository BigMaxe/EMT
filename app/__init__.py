from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from app.services.device_optimization_service import DeviceOptimizationService
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Initialize services
    app.device_optimization_service = DeviceOptimizationService

    from app.models.form import Form, FormField
    from app.models.form_response import FormResponse
    from app.models.integration import Integration
    from app.models.link_review import LinkReview
    from app.models.live_support import LiveSupportSession, Message
    from app.models.scheduling import Schedule
    from app.models.social_interactions import SocialInteraction
    from app.models.white_label import WhiteLabelSettings

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.campaign import campaign_bp
    app.register_blueprint(campaign_bp, url_prefix='/api/campaign')

    from app.routes.email_list import email_list_bp
    app.register_blueprint(email_list_bp, url_prefix='/api/email_list')

    from app.routes.email_template import email_template_bp
    app.register_blueprint(email_template_bp, url_prefix='/api/email_template')

    from app.routes.email_survey import email_survey_bp
    app.register_blueprint(email_survey_bp, url_prefix='/api/email_survey')

    from app.routes.link_review import link_review_bp
    app.register_blueprint(link_review_bp, url_prefix='/api/link_review')

    from app.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    from app.routes.ab_testing import ab_testing_bp
    app.register_blueprint(ab_testing_bp, url_prefix='/api/ab_testing')

    from app.routes.form_builder import form_builder_bp
    app.register_blueprint(form_builder_bp, url_prefix='/api/form_builder')

    from app.routes.integrations import integrations_bp
    app.register_blueprint(integrations_bp, url_prefix='/api/integrations')

    from app.routes.live_support import live_support_bp
    app.register_blueprint(live_support_bp, url_prefix='/api/live_support')

    from app.routes.social_interactions import social_interactions_bp
    app.register_blueprint(social_interactions_bp, url_prefix='/api/social_interactions')

    from app.routes.scheduling import scheduling_bp
    app.register_blueprint(scheduling_bp, url_prefix='/api/scheduling')

    from app.routes.white_label import white_label_bp
    app.register_blueprint(white_label_bp, url_prefix='/api/white_label')

    from app.routes.utils import utils_bp
    app.register_blueprint(utils_bp, url_prefix='/api/utils')

    from app.routes.automation import automation_bp
    app.register_blueprint(automation_bp, url_prefix='/api/automation')

    from app.routes.report import report_bp
    app.register_blueprint(report_bp, url_prefix='/api/report')

    from app.routes.spam_filter import spam_filter_bp
    app.register_blueprint(spam_filter_bp, url_prefix='/api/spam_filter')

    return app
