import { Component } from '@angular/core';
import { IMovie } from './movie';
import { MovieService } from './movie.service';
import {NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbdModalConfirm } from '../modal/modal';

@Component({
  selector: 'movie-recommendation',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.css']
})
export class MovieComponent {
  title = 'movie-recommendation';

  movies: IMovie[]  = [];
  steps: IMovie[][] = [];
  currentStep = 0;
  originalMovie = {} as IMovie;

  currentRecommendations: IMovie[] = [];
  constructor(private movieService: MovieService, private ngbModal: NgbModal) { }

  ngOnInit() {
    this.getMovies();
  }

  getMovies() {
    this.movieService.getAllMovies().subscribe(movies => {
      this.movies = movies;
      let modelRef = this.ngbModal.open(NgbdModalConfirm);
      modelRef.componentInstance.mode = 0;
    });
  }

  recommendMovies(movie: IMovie) {
    this.originalMovie = movie;
    this.movieService.getRecommendationFor(movie).subscribe(recommendation => {
      this.steps.push(recommendation.lda);
      this.steps.push(recommendation.bert);
      this.steps.push(recommendation.kmeans);
      this.movies = [];
      this.currentRecommendations = this.steps[this.currentStep];
    })
  }

  changeRecommendations() {
    this.currentStep += 1;
    this.currentRecommendations = this.steps[this.currentStep];
  }

  saveSelections() {
    let selectedMovies : string[] = []; 
    this.steps.forEach((movieList) => {
      selectedMovies.push(movieList.filter(movie => {
        return movie.marked == 1
      }).reduce((previous, current) => {
        return previous + ',' + current.imdb_id
      }, ''));
    });

    let body = {
      'lda': selectedMovies[0].substring(1),
      'bert': selectedMovies[1].substring(1),
      'kmeans': selectedMovies[2].substring(1),
      'original': this.originalMovie.imdb_id
    };

    this.movieService.saveUserSelection(body).subscribe(data => {
      let modalRef;
      if ('response_id' in data) {
        modalRef = this.ngbModal.open(NgbdModalConfirm);
        modalRef.componentInstance.mode = 1;
      } else {
        let modalRef = this.ngbModal.open(NgbdModalConfirm);
        modalRef.componentInstance.mode = 2;
        console.log(data['error']);
      }
      if (modalRef != undefined && (modalRef.componentInstance.mode == 1 || modalRef.componentInstance.mode == 2)) {
        modalRef.componentInstance.mode = 1;
        modalRef.result.then((data) => {
          location.reload();
        },
        (error) => {
        });
      }
    });

  }

}
