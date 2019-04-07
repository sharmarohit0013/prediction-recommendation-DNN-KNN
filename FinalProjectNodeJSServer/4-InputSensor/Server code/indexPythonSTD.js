//dont forget use Postman to send post request as JSON 

const express = require('express');
var toArray = require('stream-to-array');
var cors = require('cors')
const app = express();

app.use(cors());
//since we are parsing json which we will get from web we need below, more in later tutorials on this 
app.use(express.json());

app.get('/',(req,res)=>{
    //this callback function is also called as rout handler
    res.send("Welcome..!!");
});



//~~~~~Parameters~~~~~~

//http://localhost:3004/api/inputData

app.post('/api/inputData',(req,res) => {
	
	var result = "";
	var jsonObj;
    const InputData = {
        id:req.body.id,
        nodeInput: req.body.nodeInput,
      	alarmCondition:  "error",
      	recomendationList: req.body.recomendationList 
    }
	const spawn = require("child_process").spawn;
	//const pythonProcess = spawn('python',["./PLCNuralNetworkClassifier/4-InputSensor/Code/getResult.py",InputData.nodeInput[0],InputData.nodeInput[1],InputData.nodeInput[2],InputData.nodeInput[3],InputData.id]);
	const pythonProcess = spawn('python',["../NN-KNN-Model-Code/enforce.py",InputData.nodeInput[0],InputData.nodeInput[1],InputData.nodeInput[2],InputData.nodeInput[3],InputData.id]);
	

	pythonProcess.stdout.on('data', (data) => 
	{
		//console.log("here2"+ data);
		var strr = data.toString('utf8');//convert buffer to string
		var replaced = strr.split("'").join('"');//replace ' with " for proper json formet
		
		if(IsValidJSONString(replaced))
		{
			//console.log("ffff-3");
			var jsonContent = JSON.parse(replaced);//parse the json
			//InputData.id = jsonContent.id;
			InputData.nodeInput = jsonContent.nodeInput;
			InputData.alarmCondition = jsonContent.alarmCondition;
			//console.log("jsonContent.recomendationList = "+jsonContent.recomendationList);
			InputData.recomendationList = jsonContent.recomendationList;
		}
		res.send(InputData);
	});
	pythonProcess.stderr.on('data', function(data) {
   		console.log('stderr: ' + data);
    	//Here is where the error output goes
});
	
});


//~~ used to set new user recommendation to database
app.post('/api/updateRecommendation',(req,res) =>
{
	console.log("iiia a amajidf");
	const InputData = {
        nodeInput: req.body.nodeInput,
        userUpdatedResultDatabaseID: req.body.userUpdatedResultDatabaseID,
		userUpdatedResultStringValue: req.body.userUpdatedResultStringValue,
		alarmCondition:	req.body.alarmCondition
    }
	//console.log("req.params.id = " +InputData.alarmCondition);
	//console.log("req.params = " +InputData.userUpdatedResultStringValue);
	
	AddRowToCSVFile(InputData,res);
		
});


//~~ used to set new user sensor data in trainingSolution.csv and also updates the KNN inputs 
app.post('/api/newRecommendationForIncorrectSolution',(req,res) =>
{
	console.log("iiia a amajidf");
	const InputData = {
        nodeInput: req.body.nodeInput,		
		alarmCondition:	req.body.alarmCondition,
		enteredSolution:req.body.enteredSolution
	};

	newRecommendationForIncorrectSolution(InputData,res);	
	
		
});


//~~ used to retrain Neural Network Model  
app.post('/api/ModelRetrain',(req,res) =>
{
	console.log("ModelRetrain");
	const InputData = {
        nodeInput: req.body.nodeInput,		
		alarmCondition:	req.body.alarmCondition,
		enteredSolution:req.body.enteredSolution
	};

	ModelRetrain(InputData,res);	
	
		
});




//~~~~~initilizing the port and listening on it~~~~~
const port = process.env.PORT || 3004;

app.listen(port,()=>console.log(`listenning on ${port} port`));




//~~~~Supporting Functions~~~~~~~~
function IsValidJSONString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;

}

function AddRowToCSVFile(InputData, res) {
	var result = "Failed";
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',["AddRowToDataSet.py",InputData.nodeInput[0],InputData.nodeInput[1],InputData.nodeInput[2],InputData.nodeInput[3],InputData.alarmCondition,InputData.userUpdatedResultStringValue]);
	//console.log("here222222");
	pythonProcess.stdout.on('data', (data) => 
	{
		//console.log("here2"+ data);
		
		var strr = data.toString('utf8');//convert buffer to string
		var replaced = strr.split("'").join('"');//replace ' with " for proper json formet
		
		if(IsValidJSONString(replaced))
		{
			//console.log("ffff-3");
			var jsonContent = JSON.parse(replaced);//parse the json
			result = jsonContent.result;			
		}		
		//console.log("result = "+ result);
		res.send({"userUpdatedResultDatabaseID": InputData.userUpdatedResultDatabaseID ,"result":result});
	});
	pythonProcess.stderr.on('data', function(data) {
   		//console.log('stderr: ' + data);
		//Here is where the error output goes
		//console.log("result = "+ result);
		res.send({"userUpdatedResultDatabaseID": InputData.userUpdatedResultDatabaseID ,"result":result});
	});
	
}


function newRecommendationForIncorrectSolution(InputData, res) {
	var result = "Failed";
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',["newRecommendationForIncorrectSolution.py",InputData.nodeInput[0],InputData.nodeInput[1],InputData.nodeInput[2],InputData.nodeInput[3],InputData.alarmCondition,InputData.enteredSolution]);
	console.log("here222222");
	pythonProcess.stdout.on('data', (data) => 
	{
		console.log("here2"+ data);
		
		var strr = data.toString('utf8');//convert buffer to string
		var replaced = strr.split("'").join('"');//replace ' with " for proper json formet
		
		if(IsValidJSONString(replaced))
		{
			console.log("ffff-3");
			var jsonContent = JSON.parse(replaced);//parse the json
			result = jsonContent.result;			
		}		
		console.log("result = "+ result);
		res.send({"result":result});
	});
	pythonProcess.stderr.on('data', function(data) {
   		console.log('stderr: ' + data);
		//Here is where the error output goes
		console.log("result = "+ result);
		res.send({"result":result});
	});
	
}

function ModelRetrain(InputData, res) {
	var result = "Failed";
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',["../NN-KNN-Model-Code/NN-Trainer.py"]);
	console.log("here222222");
	pythonProcess.stdout.on('data', (data) => 
	{
		console.log("here2"+ data);
		
		var strr = data.toString('utf8');//convert buffer to string
		var replaced = strr.split("'").join('"');//replace ' with " for proper json formet
		
		if(IsValidJSONString(replaced))
		{
			console.log("ffff-3");
			var jsonContent = JSON.parse(replaced);//parse the json
			result = jsonContent.result;			
			//console.log("jsonContent.result = "+jsonContent.result);
		}		
		console.log("retrainModelStatus = "+ result);
		res.send({"retrainModelStatus":result,"reasonForError":"N/A"});
	});
	pythonProcess.stderr.on('data', function(data) {
   		console.log('stderr: ' + data);
		//Here is where the error output goes
		console.log("retrainModelStatus = "+ result);
		res.send({"retrainModelStatus":result,"reasonForError":"Error while Retraining Model"});
	});
	
}