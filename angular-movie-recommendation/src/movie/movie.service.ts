import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from './../environments/environment';
import { IMovie, IRecommendation } from "./movie";

@Injectable({
    providedIn: 'root'
})
export class MovieService {

    private api: string = environment.apiUrl;
    constructor(private http: HttpClient) { }

    private headers = new HttpHeaders();

    getAllMovies() : Observable<IMovie[]> {
        return this.http.get<IMovie[]>(this.api + 'movies');
    }

    getRecommendationFor(movie: IMovie): Observable<IRecommendation> {
        return this.http.get<IRecommendation>(this.api + `recommend/${movie.name}`)
    }

    saveUserSelection(body: any): Observable<any> {
        this.headers.set('Content-Type', 'application/json');
        return this.http.post(this.api + 'user-response', body, {headers: this.headers})
    }

}