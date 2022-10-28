export interface IMovie {
    genre: string;
    id: number;
    imdb_id: string;
    name: string;
    poster_url: string;
    marked: number;
}

export interface IRecommendation {
    bert: IMovie[];
    lda: IMovie[];
    kmeans: IMovie[];
}