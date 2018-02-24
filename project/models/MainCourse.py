from flask import Blueprint, current_app, jsonify
from project.server import db

main_course_model = Blueprint('main_course_model', __name__)

class MainCourse(db.Model):
    __tablename__ = 'maincourse'
    dish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_name = db.Column(db.String(255), nullable = False)
    dish_category = db.Column(db.String(255), nullable = False)
    dish_price = db.Column(db.Integer, nullable = False)
    img_name = db.Column(db.String(50), nullable = True)

    def get_id(self):
        return self.dish_id
    
    def to_dict(self):
        return {
                'id': self.dish_id,
                'name': self.dish_name,
                'category': self.dish_category,
                'price': self.dish_price,
                'img': self.img_name
            }
        
@main_course_model.route('/oishii/lunchdinner', methods=['GET'])
def get_lunchdinner():
    all_maincourses = MainCourse.query.all()
    categories = []
    for food in all_maincourses:
        model = food.to_dict()
        if model['category'] not in categories:
            categories.append(model['category'])
    lunchdinner_return_arr = map(lambda item: item.to_dict(), all_maincourses)
    return jsonify({
        'fooditems': lunchdinner_return_arr,
        'categories': categories
    }) 
        
        

