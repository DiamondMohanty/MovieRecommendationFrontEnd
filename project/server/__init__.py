# project/server/__init__.py


import os

from flask import Flask, jsonify, request, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from project.server.twilio_client import TwilioClient
from project.server.oishiiMail import OishiiMailer
import firebase_admin
from firebase_admin import credentials
import datetime

# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
message_client = TwilioClient()
mail_client = OishiiMailer()

# Initialize the firebase Auth
cred = credentials.Certificate('project/server/oishii-91c5e-firebase-adminsdk-vmayp-03ddf3fe8e.json')
firebase_auth = firebase_admin.initialize_app(cred) 

# Importing the models
from project.models.Breakfasts import breakfast_model
from project.models.Dishes import dish_model
from project.models.MainCourse import main_course_model
from project.models.MealDetail import meal_detail_model
from project.models.Orders import order_model
from project.models.Package import package_model
from project.models.User import user_model
from project.models.Dashboard import dashboard_api
from project.models.Package import package_model 


def create_app():

    # instantiate the app
    app = Flask(__name__)
    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)
    

    # Register the blueprint
    app.register_blueprint(breakfast_model)
    app.register_blueprint(dish_model)
    app.register_blueprint(main_course_model)
    app.register_blueprint(meal_detail_model)
    app.register_blueprint(order_model)
    app.register_blueprint(package_model)
    app.register_blueprint(user_model)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(package_model)
    
    
    # set up extensions
    
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail_client.init_app(app)
    message_client.init_app(app)
    
    
    
        
    # This is a test URL to test the mailing
    @app.route('/oishii/sendMailTest', methods=['POST'])
    def sendTestMail():
        request_data = request.get_json()
        print request_data
        error = None
        return_data = None
        if 'email' in request_data:
            emailId = request_data['email']
            mealObj = {
                "mealName": "Non Veg Meal 1",
                "mealCount": "56",
                "mealPrice": "4406"
            }
            mail_client.sendSubscriptionMail(emailId, mealObj)
            
        else:    
            error = 'Expected keys are not found in the request'
        
        return jsonify({
            'error': error,
            'data': 'Success'            
        })
        
    return app
