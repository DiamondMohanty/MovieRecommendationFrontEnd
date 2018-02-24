# project/server/models.py

from project.server import db
     
     
class Payments(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False)
    cycle_start_date = db.Column(db.DATETIME)
    cycle_end_date = db.Column(db.DATETIME)
    payment_recieved = db.Column(db.Boolean, nullable=False)
    payment_date = db.Column(db.DATETIME)
    payment_mode = db.Column(db.String(255), nullable=False)
    