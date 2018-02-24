from project.server import db, mail_client
from flask import Blueprint, current_app, jsonify
from project.models.MealDetail import UserMealDetail
from project.models.Package import Packages
import datetime
from firebase_admin.auth import AuthError
from firebase_admin import auth

user_model = Blueprint('user_model', __name__)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.TEXT, nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    phone_number = db.Column(db.String(15), nullable=False)

    def __init__(self, email, username, address, subid, phone, admin=False):
        self.email = email
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.name = username
        self.address = address
        self.subscription_id = subid
        self.phone_number = phone
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'subscription_id': self.subscription_id,
            'phone': self.phone_number,
            'email': self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)
    
    def update_details(self):
        db.session.add(self)
        db.session.commit()
    
    def save_to_firebase(self, lunch,dinner):
        
        try:
            user = auth.create_user(
                email = self.email,
                email_verified = False,
                phone_number = self.phone_number,
                password = self.email,
                display_name = self.name,
                disabled = False
            )
            self.id = user.uid
        
            db.session.add(self)
            db.session.commit()
            detail = UserMealDetail(self.id, lunch, dinner)
            detail.save()
            fetchedPack = Packages.query.filter(Packages.pack_id == int(self.subscription_id)).first().to_dict()
            mealObj = {
                "mealName": fetchedPack['name'],
                "mealCount": str(fetchedPack['meal_count']),
                "mealPrice": str(fetchedPack['price'])
            }
            mail_client.sendSubscriptionMail(self.email, mealObj)

            return None
        except ValueError as err:
            return str(err)
        except AuthError as err:
            return 'Email id already registered with us.' 
        except Exception as err:
            return 'The request could not be completed due to internal exception'  
        
@user_model.route('/oishii/newsubscription', methods=['POST'])
def save_new_subscription():
    request_data = request.get_json()
    error = None
    expected_keys = ['name', 'address', 'phone', 'subid', 'email']
    missing_keys = []
    for key in expected_keys:
        if key not in request_data:
            missing_keys.append(key)
    
    if len(missing_keys) == 0:
        
        # TODO : Validate the data
        
        newUser = User(
            request_data['email'],
            request_data['name'],
            request_data['address'],
            request_data['subid'],
            request_data['phone'],
        )
        if 'lunch' in request_data and 'dinner' not in request_data:
            exp = newUser.save_to_firebase(request_data['lunch'], 1)
        elif 'lunch' not in request_data and 'dinner'  in request_data:
            exp = newUser.save_to_firebase(0, request_data['dinner'])
        else:
            exp = newUser.save_to_firebase(request_data['lunch'], request_data['dinner'])
        if exp is not None:
            error = exp
    else:
        error = 'Expected keys are not present in the request'
    
    return jsonify({
        'error': error,
        'data': ''
    })
    
@user_model.route('/oishii/getdetails', methods=['POST'])
def get_details_for_user():
    request_data = request.get_json()
    error = None
    return_data = None
    if 'uid' not in request_data:
        error = 'Expected keys are not present in the request'
    else:
        user = User.query.filter(User.id == request_data['uid']).first()
        return_data = user.to_dict()
        
    return jsonify({
        'error': error,
        'data': return_data
    })   
    
@user_model.route('/oishii/savedetails', methods=['POST'])
def update_user():
    request_data = request.get_json()
    error = None
    status = None
    if 'details' not in request_data:
        error = 'Expected keys are not present in the request'
    else:
        user_details = request_data['details']
        user = User.query.filter(User.id == user_details['uid']).first()
        if 'subid' in user_details:
            user.subscription_id = user_details['subid']
            user.update_details() 
            status ='Success'
        else:
            user.email = user_details['email']
            user.address = user_details['address']
            user.phone = user_details['phone']
            user.update_details()
            status ='Success'
        
    
    return jsonify({
        'error': error,
        'data': status
    })   