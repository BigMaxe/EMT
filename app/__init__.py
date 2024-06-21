from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.models.form import Form, FormField
    from app.models.form_response import FormResponse
    from app.models.integration import Integration
    from app.models.link_review import LinkReview
    from app.models.live_support import LiveSupportSession, Message
    from app.models.scheduling import Schedule

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

    return app
