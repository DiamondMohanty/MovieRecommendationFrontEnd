from flask import Blueprint, current_app, jsonify
from project.server import db
import datetime

meal_detail_model = Blueprint('meal_detail_model', __name__)

class UserMealDetail(db.Model):
    __tablename__ = 'user_meal_details'
    detailid = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False)
    cycle_start_date = db.Column(db.DATETIME, default=datetime.datetime.now())
    dinner = db.Column(db.Boolean)
    lunch = db.Column(db.Boolean)
    breakfast = db.Column(db.Boolean)
    
    def __init__(self, userid, lunch, dinner):
        self.uid = userid
        self.lunch = lunch
        self.dinner = dinner        
      
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'userid': self.uid,
            'plan_start_date': self.cycle_start_date,
            'lunch': self.lunch,
            'dinner': self.dinner
        }  
    

class CancelledMealDetails(db.Model):
    __tablename__ = 'cancelled_meal_detail'
    cancel_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False)
    request_date = db.Column(db.DATETIME, default=datetime.datetime.now())
    cancel_date = db.Column(db.DATE)
    cancel_lunch = db.Column(db.Boolean)
    cancel_breakfast = db.Column(db.Boolean)
    cancel_dinner = db.Column(db.Boolean)
    reason = db.Column(db.TEXT, nullable=True)
    
    def __init__(self, userid, cancel_date, lunch, dinner, breakfast, reason):
        self.uid = userid
        self.cancel_date = cancel_date
        self.cancel_lunch = lunch
        self.cancel_dinner = dinner
        self.cancel_breakfast = breakfast
        self.reason = reason
    
    def to_dict(self):
        return {
            'uid': self.uid,
            'request_date': self.request_date,
            'cancel_date': self.cancel_date,
            'lunch': self.cancel_lunch,
            'breakfast': self.cancel_breakfast,
            'dinner': self.cancel_dinner,
            'reason': self.reason
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
@meal_detail_model.route('/oishii/requestcancel', methods=['POST'])
def request_meal_cancellation():
    request_data = request.get_json()
    error = None
    status = None
    request_arr = request_data['records']
    for obj in request_arr:
        user_id = obj['userid']
        lunch = obj['lunch']
        dinner = obj['dinner']
        breakfast = 0
        reason = obj['reason']
        date = common.date_from_string(obj['date'])
        newCancelModel = CancelledMealDetails(user_id, date, lunch, dinner, breakfast, reason)
        newCancelModel.save()
    
    return jsonify({
        'error': error,
        'status': status
    })
        
@meal_detail_model.route('/oishii/cancellationRequests', methods=['POST'])
def get_cancellation_request():
    request_data = request.get_json()
    error = None
    return_data = None
    if 'uid' in request_data:
        query_response = CancelledMealDetails.query.filter(CancelledMealDetails.uid == request_data['uid']).filter(CancelledMealDetails.cancel_date >= datetime.datetime.now()).all()
        return_data = map(lambda ele: ele.to_dict(), query_response)
    else:
        error = 'Expected keys are not present in the request'
        
    return jsonify({
        'error': error,
        'data': return_data
    })