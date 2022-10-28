import pickle
from typing import List
from project.models.movies import Movies
import numpy as np
from project.server import db

class LdaTrainer():

    def __init__(self) -> None:
        with open('trained_models/lda/lda_model.pkl', 'rb') as fd:
            self.__model = pickle.load(fd)
        
        with open('trained_models/lda/corpus.pkl', 'rb') as fd:
            self.__corpus = pickle.load(fd)

        with open('trained_models/lda/lda_data.pkl', 'rb') as fd:
            self.__data = pickle.load(fd)

    def predict(self, movie_name: str) -> List[Movies]:
        found_movie_idx = None
        for idx, movie in enumerate(self.__data):
            if movie['original_title'] == movie_name:
                found_movie_idx = idx
        
        if found_movie_idx is not None:
            corpus = self.__corpus[found_movie_idx]
            preds = self.__model.get_document_topics(corpus)
            prob_high = -1
            pred_topic = None
            for p in preds:
                if p[1] > prob_high:
                    prob_high = p[1]
                    pred_topic = p[0]
            
            pred_tupple = (pred_topic, prob_high)
            initial_recommendations = []
            recommendation_probabilties = [] 

            for movie in self.__data:
                if movie['topic'][0] == pred_tupple[0]:
                    initial_recommendations.append(movie)
                    recommendation_probabilties.append(movie['topic'][1])

            imdb_ids = [] 
            sorted_indices = np.argsort(recommendation_probabilties)
            for idx in sorted_indices:
                if movie_name != initial_recommendations[idx]['original_title']:
                    imdb_ids.append(initial_recommendations[idx]['imdb_id'])
        
            return db.session.query(Movies).filter(Movies.imdb_id.in_(imdb_ids)).all()

            

        

    