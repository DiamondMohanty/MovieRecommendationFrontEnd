from flask import Blueprint, jsonify
from project.services import movie_service

movie_controller = Blueprint('movie_controller', __name__)

@movie_controller.route('/api/movies', methods=['GET'])
def get_all():
    response = movie_service.get_all_movies()
    return jsonify(response), 200

@movie_controller.route('/api/recommend/<in_movie>', methods=['GET'])
def recommend_movie(in_movie):
    response = movie_service.get_recommendation_for(in_movie)
    return jsonify(response), 200