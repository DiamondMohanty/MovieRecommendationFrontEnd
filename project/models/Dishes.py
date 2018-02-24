from project.server import db
from flask import Blueprint, current_app, jsonify

dish_model = Blueprint('dish_model', __name__)

class Dishes(db.Model):
    
    __tablename__ = 'popular_dishes'
    dish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_name = db.Column(db.String(255), nullable = False)
    dish_price = db.Column(db.Integer, nullable = False)
    dish_items = db.Column(db.TEXT, nullable = False)
    dish_type = db.Column(db.String(15), nullable = False)
    img_name = db.Column(db.String(50), nullable = True)
    
    def get_id(self):
        return self.dish_id
    
    def __repr__(self):
        return '<Dishes {0}>'.format(self.dish_name)
    
    def to_dict(self):
        return {
                'id': self.dish_id,
                'name': self.dish_name,
                'price': self.dish_price,
                'items': self.dish_items,
                'type': self.dish_type,
                'img': self.img_name
            }
        
@dish_model.route('/oishii/highlightdish', methods=["GET"])
def get_dishes():
    all_dishes = Dishes.query.all()
    dish_list = map(lambda item: item.to_dict(), all_dishes)
    return jsonify(dish_list)
    