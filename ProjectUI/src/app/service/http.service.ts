import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class HttpService 
{  
    //private recivedResult$: Subject<Array<DetailsDemo>> = new BehaviorSubject<Array<DetailsDemo>>([]);
  //cast = this.recivedResult.asObservable();
  dataBaseIdCounter:number = 9999;
  todos: Observable<DetailsDemo[]>
  private _receivedData: BehaviorSubject<DetailsDemo[]>;
  private receivedDataStore: {
    todos: DetailsDemo[]
  };

  constructor(private httpClient:HttpClient) { 
    this.receivedDataStore = { todos: [] };
    this._receivedData = <BehaviorSubject<DetailsDemo[]>>new BehaviorSubject([]);
    this.todos = this._receivedData.asObservable();
  }
  //POST method
  putNewSollutionInDB(userInput: DetailsDemo, enteredSolution: any): any {
    this.httpClient.post("http://localhost:3004/api/newRecommendationForIncorrectSolution",{
      nodeInput:          userInput.nodeInput,
      alarmCondition:     "1",
      enteredSolution:    enteredSolution,
    }).subscribe((data:any)=>
    {
      console.log("userUpdatedResultDatabaseID: " +data.enteredSolution);
      console.log("result = " + data.result);
    },
    (err: any) => {
      console.error("putNewSollutionInDB: ERROR");
    }
    );
  }

  //POST Method
  postNewUserInputToServer( userInputsLength, newUserInput)
  {
    this.httpClient.post("http://localhost:3004/api/inputData",{
      id:                 userInputsLength,
      nodeInput:          newUserInput.nodeInput,
      alarmCondition:     "N/A",
      recomendationList:  "N/A"
    }).subscribe((data:any)=>
    {

      this.receivedDataStore.todos.push(data);
      console.log("this.receivedDataStore "+ data.recomendationList[0].databaseID);
      this._receivedData.next(Object.assign({}, this.receivedDataStore).todos);     
    },
    (err: any) => {
      console.error("postNewUserInputToServer: ERROR")
      newUserInput.alarmCondition = "Server Error";
      this.receivedDataStore.todos.push(newUserInput);
      console.log("this.newUserInput "+ newUserInput.id);
      this._receivedData.next(Object.assign({}, this.receivedDataStore).todos);
    }
    );
  }
  //POST Method
  postUpdatedRecomendationToServer(updatedData:DetailsDemo)
  {
    if(updatedData.userUpdatedResultDatabaseID === -1)
    {
      updatedData.userUpdatedResultDatabaseID = this.dataBaseIdCounter;
      this.dataBaseIdCounter++;
    }
    console.log("updatedData.alarmCondition = "+updatedData.alarmCondition);
    this.httpClient.post("http://localhost:3004/api/updateRecommendation",{
      nodeInput                     : updatedData.nodeInput,
      userUpdatedResultDatabaseID   : updatedData.userUpdatedResultDatabaseID,
      userUpdatedResultStringValue  : updatedData.userUpdatedResultStringValue,
      alarmCondition                : "1"
    }).subscribe((data:any)=>
    {
      console.log("userUpdatedResultDatabaseID: " +data.userUpdatedResultDatabaseID);
      console.log("result = " + data.result);
    },
    (err: any) => {
      console.error("postNewUserInputToServer: ERROR");
    }
    );
  }
  //POST Method
  postModelRetrainRequest(){
    this.httpClient.post("http://localhost:3004/api/ModelRetrain",{
      retrainModelStatus:   "Failed",
      reasonForError:        "Unknown"
    }).subscribe((data:any)=>
    {
      console.log("retrainModelStatus: " +data.retrainModelStatus);
      console.log("reasonForError = " + data.reasonForError);
    },
    (err: any) => {
      console.error("postModelRetrainRequest: ERROR");
    }
    );
  }
}

export interface recomendationlistDetails{
  resultID: number;
  result: string 
}
export class abc implements recomendationlistDetails{
  resultID:number =1;
  databaseID:number      =-1;
  result:"";
}
export class DetailsDemo{
    id: number   =              1;
    nodeInput:                  [""];
    displayInputNode:string =   "";
    alarmCondition:string   =   "Processing";
    recomendationList:          [abc];
    userUpdatedResultDatabaseID:number=  -1;
    userUpdatedResultStringValue: "";
    constructor(userInput)
    {
      this.nodeInput = userInput;
      this.displayInputNode = "--> " + userInput[0]
      for(var i = 1;i<userInput.length;i++){
        console.log("userInput[] = "+userInput[i]);
        this.displayInputNode = this.displayInputNode + " , " + userInput[i] ;
      }
    }
}