from flask import Blueprint, current_app, jsonify
from project.server import db, message_client
import datetime
from project.server import common

order_model = Blueprint('order_model', __name__)

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(10), nullable = True, default='Pending')
    order_cust_name = db.Column(db.String(255), nullable = False)
    order_cust_addr = db.Column(db.String(255), nullable = False)
    order_cust_email = db.Column(db.String(255), nullable = True)
    order_cust_phone = db.Column(db.String(255), nullable = False)
    order_items = db.Column(db.TEXT, nullable = False)
    order_date = db.Column(db.DATETIME, nullable = False, default=datetime.datetime.now()) 
    order_paid = db.Column(db.Boolean, nullable = False, default=False)
    
    def __init__(self, cust_name, cust_addr, cust_email, cust_phone, items):
        self.order_cust_name = cust_name
        self.order_cust_addr = cust_addr
        self.order_cust_email = cust_email
        self.order_items = items
        self.order_cust_phone = cust_phone
        
    
    def get_id(self):
        return self.order_id

@order_model.route('/oishii/placeorder', methods=['POST'])
def place_order():
    request_data = request.get_json()
    customer = request_data['customer']
    
    # Generate Full Address
    complete_addr = ''
    valid_keys = ['addr1', 'addr2', 'landmark']
    for key in valid_keys:
        if key in customer:
            complete_addr += customer[key]
            
    # Checking if the keys are present in the customer data
    customer_name = ''
    customer_phone = ''
    customer_email = ''
    csv_ordered_items = ''
    
    if 'name' in customer:
        customer_name = customer['name']
    
    if 'phone' in customer:
        customer_phone = customer['phone']
        
    if 'email' in customer:
        customer_email = customer['email']
    
    if 'items' in request_data:
        ordered_items = request_data['items']
        for item in ordered_items:
            csv_ordered_items += item['name'] + '(' + str(item['qty']) + '),'
        csv_ordered_items = csv_ordered_items.rstrip(',')
    
    new_order = Orders(customer_name, complete_addr, customer_email, customer_phone, csv_ordered_items)
                 
    db.session.add(new_order)
    db.session.commit()
    
    sms_message = common.generate_message_body(request_data['items'], complete_addr, customer_name, customer_phone)
    message_client.sendMessage('+919583703079', '+12392014801 ', sms_message)
    
    return jsonify({'status': 200})