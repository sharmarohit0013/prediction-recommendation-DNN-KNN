import { Component, OnInit,Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
import { DetailsDemo,HttpService} from './../service/http.service';

@Component({
  selector: 'app-retrain-model',
  templateUrl: './retrain-model.component.html',
  styleUrls: ['./retrain-model.component.css']
})
export class RetrainModelComponent implements OnInit {

  constructor( public dialogRef: MatDialogRef<RetrainModelComponent>, private httpService: HttpService,
    @Inject(MAT_DIALOG_DATA) public data: DetailsDemo)
  {}
  onNoClick(): void {
    this.dialogRef.close();
  }
  startRetraining():void{
    this.httpService.postModelRetrainRequest();
    this.dialogRef.close();
  }


  ngOnInit() {
  }

}
