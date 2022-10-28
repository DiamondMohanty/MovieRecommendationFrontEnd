from project.models.user_response import UserReponses


def save_user_response(response):
    new_user_response = UserReponses()
    new_user_response.lda_model = response['lda']
    new_user_response.k_means_model = response['kmeans']
    new_user_response.original = response['original']
    new_user_response.bert_model = response['bert']
    return new_user_response.save()