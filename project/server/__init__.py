# project/server/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()

from project.controllers import controllers

def create_app():
    # instantiate the app
    app = Flask(__name__)
    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)
    
    # Registering the controllers
    for controller in controllers:
        app.register_blueprint(controller)

    # set up extensions
    db.init_app(app)
    return app

