from project.server import db

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable = False)
    genre = db.Column(db.String(255), nullable = False)
    imdb_id = db.Column(db.String(255), nullable = False, unique = True)
    poster_url = db.Column(db.String(255), nullable = True)
    
    def get_id(self):
        return self.id
        
    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'genre': self.genre,
                'imdb_id': self.imdb_id,
                'poster_url': self.poster_url
            }
        

    