from project.models.movies import Movies
from typing import List
from project.trainers import kmeans_trainer, lda_trainer, bert_trainer

k_means_model = kmeans_trainer.KMeansTrainer()
lda_model = lda_trainer.LdaTrainer()
bert_model = bert_trainer.BertTrainer()

K_TOP_MOVIES = 10

def get_all_movies() -> List[Movies]:
    all_movies = Movies.query.all()
    return [movie.to_dict() for movie in all_movies]
    

def get_recommendation_for(in_movie: str) -> List[Movies]:
    kmeans_preds = k_means_model.predict(in_movie)
    lda_preds = lda_model.predict(in_movie)
    bert_preds = bert_model.predict(in_movie)
    return [
        {
            'kmeans': [movie.to_dict() for movie in kmeans_preds][len(kmeans_preds) - K_TOP_MOVIES:],
            'lda': [movie.to_dict() for movie in lda_preds][len(lda_preds) - K_TOP_MOVIES:],
            'bert': [movie.to_dict() for movie in bert_preds][len(bert_preds) - K_TOP_MOVIES:]
        }
    ]
