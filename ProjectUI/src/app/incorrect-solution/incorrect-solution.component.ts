import { Component, OnInit,Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
import { DetailsDemo,HttpService} from './../service/http.service';

@Component({
  selector: 'app-incorrect-solution',
  templateUrl: './incorrect-solution.component.html',
  styleUrls: ['./incorrect-solution.component.css']
})
export class IncorrectSolutionComponent implements OnInit {

  constructor( public dialogRef: MatDialogRef<IncorrectSolutionComponent>, private httpService: HttpService,
    @Inject(MAT_DIALOG_DATA) public data: DetailsDemo)
  {}
  addUserSolution(enteredSolution){
    if(enteredSolution)
    {
      //call a put request here
      this.httpService.putNewSollutionInDB(this.data,enteredSolution);
    }

    this.dialogRef.close();
  }
  
  onNoClick(): void {
    this.dialogRef.close();
  }
  ngOnInit() {
  }

}
