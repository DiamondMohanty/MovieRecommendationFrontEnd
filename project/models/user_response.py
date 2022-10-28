from project.server import db

class UserReponses(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lda_model = db.Column(db.String(255), nullable = False)
    k_means_model = db.Column(db.String(255), nullable = False)    
    bert_model = db.Column(db.String(255), nullable = False)
    original = db.Column(db.String(255), nullable = False)

    def get_id(self):
        return self.id
        
    def to_dict(self):
        return {
                'id': self.id,                
                'lda': self.lda_model,
                'kmeans': self.k_means_model,                
                'bert': self.bert_model,                
                'original': self.original
            }
    
    def save(self):
        self.id = len(UserReponses.query.all()) + 1
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            return str(e)

