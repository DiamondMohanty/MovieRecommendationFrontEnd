from project.server import db
from flask import Blueprint, jsonify

user_response_model = Blueprint('user_response_model', __name__)

class UserReponses(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(255), nullable = False)
    lda_model = db.Column(db.String(255), nullable = False)
    k_means_model = db.Column(db.String(255), nullable = False)
    cosine_model = db.Column(db.String(255), nullable = True)
    bert_model = db.Column(db.String(255), nullable = True)
    default_model = db.Column(db.String(255), nullable = True)

    def get_id(self):
        return self.id
        
    def to_dict(self):
        return {
                'id': self.id,
                'user': self.user_email,
                'lda': self.lda_model,
                'k-means': self.k_means_model,
                'cosine': self.cosine_model,
                'bert': self.bert_model,
                'default': self.default_model
            }
        

@user_response_model.route('/api/user-response', methods=['POST'])
def save_user_response():
    pass
