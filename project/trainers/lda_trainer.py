import pickle
from typing import List
from project.models.movies import Movies
import numpy as np
from project.server import db

class LdaTrainer():

    def __init__(self) -> None:
        with open('trained_models/lda/lda_model.pkl', 'rb') as fd:
            self.__model = pickle.load(fd)
        
        with open('trained_models/lda/vocab.pkl', 'rb') as fd:
            self.__id2word = pickle.load(fd)

        with open('trained_models/lda/lda_data.pkl', 'rb') as fd:
            self.__data = pickle.load(fd)

    def predict(self, movie_name: str) -> List[Movies]:
        test_corpus = self.__id2word.doc2bow([movie_name])
        preds = self.__model.get_document_topics(test_corpus)
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
            imdb_ids.append(initial_recommendations[idx]['imdb_id'])

        return db.session.query(Movies).filter(Movies.imdb_id.in_(imdb_ids)).all()

            

        

    