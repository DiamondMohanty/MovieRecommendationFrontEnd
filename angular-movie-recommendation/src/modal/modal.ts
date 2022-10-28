import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
	selector: 'ngbd-modal-confirm',
	template: `
		<div class="modal-header">
			<strong>Instructions</strong>
		</div>
		<div class="modal-body">
			<ol *ngIf='mode == 0'>
				<li>Select a movie. (Click on movie poster)</li>
				<li>You will be presented with 3 set of movies</li>
				<li>In each set check the movies by clicking on the checkbox beside the movie title which you think is similar to the movie you selected in step 1</li>
				<li>Click on submit to send your selections.</li>
			</ol>
			<p *ngIf='mode == 1' class=" text-center">
				<strong>Thank You 👍</strong>
			</p>
			<p *ngIf='mode == 2' class=" text-center">
				<strong>Internal exception occured 🙁. Please try again.</strong>
			</p>
		</div>
		<div class="modal-footer">
			<button type="button" class="btn btn-danger" (click)="modal.close('Ok click')">Ok</button>
		</div>
	`
})
export class NgbdModalConfirm {
	constructor(public modal: NgbActiveModal) {}
	mode = 0
}