import pickle
from project.models.movies import Movies
import numpy as np
from project.server import db

class KMeansTrainer():

    def __init__(self) -> None:
        with open('trained_models/kmeans/kmeans_out.pkl', 'rb') as fd:
            self.__model = pickle.load(fd)
            
    def __similar(self, original: str, target: str) -> int:
        a = set(original.split('|'))
        b = set(target.split('|'))
        return len(a.intersection(b))

    def predict(self, movie_name: str):
        movies = list(filter(lambda ele: ele['original_title'] == movie_name, self.__model))
        if len(movies) == 1:
            found_movie = movies[0]
            cluster = found_movie['kmeans_pred']
            may_be_movies = list(filter(lambda ele: ele['kmeans_pred'] == cluster and ele['original_title'] != movie_name, self.__model))
            imdb_ids = []
            for m in may_be_movies:
                if m['imdb_id'] != found_movie['imdb_id']:
                    imdb_ids.append(m['imdb_id'])
            initial_recommendation = db.session.query(Movies).filter(Movies.imdb_id.in_(imdb_ids)).all()
            db_movie = Movies.query.filter_by(name = movie_name).first()
            final_movies = []
            genre_distances = []
            for m in initial_recommendation:
                genre_distances.append(self.__similar(db_movie.genre, m.genre))

            sorts = np.argsort(genre_distances)

            for idx in sorts:
                final_movies.append(initial_recommendation[idx])

            return final_movies