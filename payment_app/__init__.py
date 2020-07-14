import os
from flask import Flask
from flask_migrate import Migrate


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    from .config import Config
    app.config.from_object(Config)

    from .models import db
    db.init_app(app)

    migrate.init_app(app, db)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from payment_app.views import payment_bp
    app.register_blueprint(payment_bp)

    return app
