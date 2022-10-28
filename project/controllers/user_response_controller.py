from flask import Blueprint, request, jsonify
from project.services import user_response_service

user_response_controller = Blueprint('user_response_controller', __name__)

@user_response_controller.route('/api/user-response', methods=['POST'])
def save_responses():
    data = request.get_json()
    response = user_response_service.save_user_response(data)
    if isinstance(response, int):
        return jsonify({'response_id': response})
    else:
        return jsonify({'error': response})
