import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { MovieComponent } from '../movie/movie.component';
import { MovieThumbnailComponent } from '../movie/movie-thumbnail-component';
import { NgbdModalConfirm } from '../modal/modal';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    MovieComponent,
    MovieThumbnailComponent,
    NgbdModalConfirm
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgbModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [MovieComponent]
})
export class AppModule { }
