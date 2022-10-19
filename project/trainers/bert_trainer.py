import pickle
from typing import List
from project.models.movies import Movies
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from project.server import db

class BertTrainer():
    def __init__(self):
        with open('trained_models/bert/bert_embedding.pkl', 'rb') as fd:
            self.__embeddings = pickle.load(fd)
        
        with open('trained_models/bert/bert_data.pkl', 'rb') as fd:
            self.__bert_data = pickle.load(fd)

    
    def predict(self, in_movie: str) -> List[Movies]:
        in_movie_idx = None
        
        for idx, movie in enumerate(self.__bert_data):
            if movie['original_title'] == in_movie:
                in_movie_idx = idx
                break
        
        remaining_embedds = []
        for idx, embed in enumerate(self.__embeddings):
            if idx != in_movie_idx:
                remaining_embedds.append(embed)

        similarities = cosine_similarity(
            [self.__embeddings[in_movie_idx]],
            remaining_embedds
        )

        sorted_idx = np.argsort(similarities[0])
        imdb_ids = []
        for idx in sorted_idx:
            imdb_ids.append(self.__bert_data[idx]['imdb_id'])

        

        return db.session.query(Movies).filter(Movies.imdb_id.in_(imdb_ids)).all()