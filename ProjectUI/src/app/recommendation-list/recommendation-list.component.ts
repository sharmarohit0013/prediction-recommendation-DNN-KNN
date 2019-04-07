import { Component, OnInit,Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
import { DetailsDemo,HttpService} from './../service/http.service';

@Component({
  selector: 'app-recommendation-list',
  templateUrl: './recommendation-list.component.html',
  providers: [HttpService],
  styleUrls: ['./recommendation-list.component.css']
})
export class RecommendationListComponent implements OnInit {
  selectedRow : Number =0;
  setClickedRow : Function;

  constructor( public dialogRef: MatDialogRef<RecommendationListComponent>, private httpService: HttpService,
                 @Inject(MAT_DIALOG_DATA) public data: DetailsDemo)
  {
    this.setClickedRow = function(index)
    {
      this.selectedRow = index;
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSendSuggestionClick(userSuggestion) : void 
  {
    var isPost = false;
    console.log("userSuggestion = "+userSuggestion);
    if(userSuggestion[0] != 1 && userSuggestion[1] ==="")//if user have chosen from Recommendation list and ID != 1
    {
      this.data.recomendationList.forEach(recomendation =>{
        console.log("hello "+recomendation.resultID);
        if(recomendation.resultID === userSuggestion[0])
        {
          this.data.userUpdatedResultDatabaseID = recomendation.databaseID;
          this.data.userUpdatedResultStringValue = recomendation.result;
          isPost = true;          
        }
      });     
    }
    else if (userSuggestion[1])
    {
      console.log("isPost [1]");
      isPost = true;
      this.data.userUpdatedResultStringValue = userSuggestion[1];
    }
    if(isPost)
    {
      console.log("isPost true");
      this.httpService.postUpdatedRecomendationToServer(this.data);
    }
    this.dialogRef.close();
  }
  ngOnInit() {
  }

}
