from flask import Blueprint, current_app, jsonify
from project.server import db

package_model = Blueprint('package_model', __name__)

class Packages(db.Model):
    __tablename__ = 'packs'
    pack_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pack_name = db.Column(db.String(50), nullable = False)
    pack_items = db.Column(db.TEXT, nullable = False) 
    pack_price = db.Column(db.Integer, nullable = False)
    pack_meal_count = db.Column(db.Integer, nullable = False)
    pack_active = db.Column(db.Boolean, nullable = False, default = False)
    pack_per_meal_price = db.Column(db.Integer, nullable = False) 
    pack_plan = db.Column(db.String(50), nullable = False) 
    
    def get_id(self):
        return self.pack_id
    
    def to_dict(self):
        return {
            'id': self.pack_id,
            'name': self.pack_name,
            'items': self.pack_items,
            'price': self.pack_price,
            'active': self.pack_active,
            'meal_count': self.pack_meal_count,
            'per_meal_price': self.pack_per_meal_price,
            'plan': self.pack_plan
        }

class PackageMaster(db.Model):
    __tablename__ = 'package_master'
    pack_name = db.Column(db.String(50), nullable = False, primary_key = True)
    
    def to_dict(self):
        return {
            'pack_name': self.pack_name
        }
        
    def repr(self):
        return self.pack_name        
        
        
@package_model.route('/oishii/recommenedsub', methods=['GET'])
def get_recommened_subscriptions():
     all_packs = Packages.query.filter(Packages.pack_id.in_((1,8,10))).all() 
     packages = map(lambda item: item.to_dict(), all_packs)
     for pack in packages:
            pack['items'] = pack['items'].split(',')
     return jsonify(packages) 

@package_model.route('/oishii/packs', methods=['GET'])
def get_packs():
    all_packs = Packages.query.all()
    packages = map(lambda item: item.to_dict(), all_packs)
    
    all_packs_names = PackageMaster.query.all()
    packages_names = map(lambda item: item.repr(), all_packs_names)
    
    # Creating the package name and package items mapping
    mapping_dict = {}
    for pack in packages:
        pack['items'] = pack['items'].split(',')
        if pack['name'] in packages_names:
            mapping_dict[pack['name']] = pack['items']
                  
    
    
    return jsonify({
            'packages': packages,
            'names': packages_names,
            'mapping': mapping_dict
        })
    
@package_model.route('/oishii/pack', methods=['POST'])
def get_pack_by_id():
    request_data = request.get_json()
    error = None
    return_data = None
    if 'id' in request_data:
        in_pack_id = request_data['id']
        fetched_pack = Packages.query.filter(Packages.pack_id == int(in_pack_id)).first()
        if fetched_pack is not None:
            return_data = fetched_pack.to_dict()
            return_data['items'] = return_data['items'].split(',')
    else:
        error = 'Invalid request recieved. Please check the in parameter name.'
        
    return jsonify(
        {
            'data': return_data,
            'error': error
        }
    )