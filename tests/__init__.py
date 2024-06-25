def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    # other initializations...

    # Register blueprints
    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # other blueprints...

    return app
