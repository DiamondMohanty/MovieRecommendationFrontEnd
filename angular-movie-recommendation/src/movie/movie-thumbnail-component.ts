import { Component, EventEmitter, Input, Output } from "@angular/core";
import { IMovie } from "./movie";

@Component({
    template:`
    <div>
        <img [src]="movie.poster_url" class="img-fluid img-thumbnail" alt="No Preview" (click)="recommendMovie()"/>
        <p class="text-center">{{movie.name}} 
        <input type="checkbox" (click)="setSelected(movie)" *ngIf="mode == 1"/> 
        </p> 
    </div>
    `,
    selector: 'movie-thumbnail',
    styles: [`
        div {
            width: 200px;
            cursor: pointer;
        }
    `]
})
export class MovieThumbnailComponent {
    @Input() movie: IMovie = {} as IMovie;
    @Input() mode: number = 1;
    @Output() select = new EventEmitter();

    recommendMovie() {
        this.select.emit(this.movie);
    }

    setSelected(movie: IMovie) {
        if (movie.marked == undefined || movie.marked == 0) {
            movie.marked = 1;
        } else {
            movie.marked = 0
        }
    }
}