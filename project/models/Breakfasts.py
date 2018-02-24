from project.server import db
from flask import Blueprint, current_app, jsonify

breakfast_model = Blueprint('breakfast_model', __name__)

class BreakFasts(db.Model):
    
    __tablename__ = 'breakfasts'
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
        

@breakfast_model.route('/oishii/addons', methods=['GET'])
def get_addons():
    all_addons = BreakFasts.query.filter(BreakFasts.dish_category == 'Addon').all()
    addon_list = map(lambda item: item.to_dict(), all_addons)
    return jsonify(addon_list)

@breakfast_model.route('/oishii/breakfasts', methods=['GET'])
def get_breakfasts():
    all_breakfasts = BreakFasts.query.all()
    categories = []
    for breakfast in all_breakfasts:
        model = breakfast.to_dict()
        if model['category'] not in categories:
            categories.append(model['category'])
    breakfast_return_arr = map(lambda item: item.to_dict(), all_breakfasts)
    
    return jsonify({
        'fooditems': breakfast_return_arr,
        'categories': categories
    }) 