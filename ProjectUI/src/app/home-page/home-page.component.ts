import { RecommendationListComponent } from './../recommendation-list/recommendation-list.component';
import { HttpService, DetailsDemo, abc, recomendationlistDetails } from './../service/http.service';
import { Component, OnInit } from '@angular/core';
import { map } from 'rxjs/operators';
import {MatDialog, MatDialogConfig} from "@angular/material";
import { Observable } from 'rxjs';
import { IncorrectSolutionComponent } from '../incorrect-solution/incorrect-solution.component';
import { RetrainModelComponent } from '../retrain-model/retrain-model.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  providers: [HttpService],
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  idCounter:number;
  name:string = "";
  userInputs: Array<DetailsDemo>;
  recivedResult:Observable<DetailsDemo[]>;
  singlerecivedResult$:Observable<DetailsDemo>;
  constructor(public dialog: MatDialog, private httpService: HttpService){
      this.userInputs = [];
      this.idCounter = 0;
  }
  
  addUserInput(userInput){
      this.idCounter++;
      let result;
      let userInputData = new DetailsDemo(userInput);
      userInputData.id = this.idCounter;
      this.userInputs.push(userInputData);
      this.httpService.postNewUserInputToServer(this.idCounter,userInputData);

  }
  EvaluateAgain(userInput){
    let index = this.userInputs.indexOf(userInput);
    this.userInputs[index].alarmCondition = "Processing";
    if(this.userInputs[index].recomendationList){
      this.userInputs[index].recomendationList.forEach(recomendation =>{
        recomendation.result = "";
        recomendation.databaseID = -1;
        recomendation.resultID = 1;
    });
  }
    console.log("here");
    this.httpService.postNewUserInputToServer(userInput.id,userInput);
  }

  removeUserInput(userInput){
    let index = this.userInputs.indexOf(userInput);
    this.userInputs.splice(index,1);
  }
  ngOnInit() {
    
    this.recivedResult = this.httpService.todos; // subscribe to entire collection

    // subscribe to only one todo 
    this.singlerecivedResult$ = this.httpService.todos.pipe(
      map(todos => todos.find(item => item.id === 1))
    );
    
    this.recivedResult.forEach(elements => {
      elements.forEach(element =>{
        //console.log("userInput.id = "+ userInput.id +" element.alarmCondition = "+ element.alarmCondition);
        this.userInputs.forEach((userInputElement,index) =>
        {          
          if(element.id === userInputElement.id){
            //console.log("element.id "+ element.id + "element.alarmCondition = "+element.alarmCondition);
            this.userInputs[index].alarmCondition = element.alarmCondition;
            this.userInputs[index].recomendationList = element.recomendationList;
          }
      })      
    })
  });
  }
  openDialogProposedRecomendation(userInput): void {
    const dialogConfig = new MatDialogConfig();

    //dialogConfig.disableClose = false;
    //dialogConfig.autoFocus = true;

    let index = this.userInputs.indexOf(userInput);
    console.log("index = "+this.userInputs[index].recomendationList[0].resultID+ " -"+this.userInputs[index].displayInputNode);
    dialogConfig.data = this.userInputs[index];
    const dialogRef = this.dialog.open(RecommendationListComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
  openDialogIncorrectSolution(userInput): void {
    const dialogConfig = new MatDialogConfig();

    //dialogConfig.disableClose = false;
    //dialogConfig.autoFocus = true;

    let index = this.userInputs.indexOf(userInput);
    console.log("index = "+this.userInputs[index].recomendationList[0].resultID+ " -"+this.userInputs[index].displayInputNode);
    dialogConfig.data = this.userInputs[index];
    const dialogRef = this.dialog.open(IncorrectSolutionComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
  openDialogRetrainModel(): void {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.data = "retrain";
    const dialogRef = this.dialog.open(RetrainModelComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

}