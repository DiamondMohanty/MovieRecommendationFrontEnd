from flask import Blueprint, current_app, jsonify
from project.models.MealDetail import CancelledMealDetails, UserMealDetail
from project.models.User import User
from project.models.Package import Packages
import datetime

dashboard_api = Blueprint('dashboard_api', __name__)

@dashboard_api.route('/oishii/dashboardoverview', methods=['POST'])
def get_member_details():
    request_data = request.get_json()
    error = None
    member_data = None
    pack_data  = None
    plan_status = None
    cancellation_data = None
    
    if 'uid' not in request_data:
       error = 'Expected keys are not present in the request'   
    else:
        fetched_user = User.query.filter(User.id == request_data['uid']).first()  
        member_data = fetched_user.to_dict()
        fetched_pack = Packages.query.filter(Packages.pack_id == int(member_data['subscription_id'])).first() 
        pack_data = fetched_pack.to_dict() 
        fetched_plan = UserMealDetail.query.filter(UserMealDetail.uid == request_data['uid']).first()
        plan_status = { 
            'start_date': fetched_plan.to_dict()['plan_start_date'],
            'lunch': fetched_plan.to_dict()['lunch'],
            'dinner': fetched_plan.to_dict()['dinner'],
        }        
        cancelled_meals = CancelledMealDetails.query.join(UserMealDetail, UserMealDetail.uid == CancelledMealDetails.uid).filter(CancelledMealDetails.uid == request_data['uid']).filter(UserMealDetail.cycle_start_date <= CancelledMealDetails.request_date).filter(CancelledMealDetails.cancel_date <= datetime.datetime.now()).order_by(CancelledMealDetails.request_date.asc()).all()[:10]
        cancellation_data = map(lambda ele: ele.to_dict(), cancelled_meals)
            
        
    return jsonify({
        'error': error,
        'member_data': member_data,
        'pack_data': pack_data,
        'plan_status': plan_status,
        'cancellation_data': cancellation_data
    })