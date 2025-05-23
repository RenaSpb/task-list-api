from flask import Flask
from .db import db, migrate
from .models import task, goal
from .routes.task_routes import tasks_bp
from .routes.goal_routes import goals_bp 
from .routes.base_routes import base_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(base_bp)
    

    return app
    