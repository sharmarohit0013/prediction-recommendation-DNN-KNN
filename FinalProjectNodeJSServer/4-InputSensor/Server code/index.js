//dont forget use Postman to send post request as JSON 

const express = require('express');
const app = express();

//since we are parsing json which we will get from web we need below, more in later tutorials on this 
app.use(express.json());

const cources = [
    {id:1,nodeInput:["abc","a"],alarmCondition:"yes",recomendationList:["do this","so that","and do"]},
     {id:2,nodeInput:["pqr","s"],alarmCondition:"no",recomendationList:["non","b","v"]},
     {id:3,nodeInput:["xyz","d"],alarmCondition:"yes",recomendationList:["non","c","v"]}
];
app.get('/',(req,res)=>{
    //this callback function is also called as rout handler
    res.send("Welcome..!!");
});
//the function able is also called as a route handler

app.get('/api/cources',(req,res)=>{
    res.send([1,2,3]);
});


//~~~~~Parameters~~~~~~

//http://localhost:3004/api/inputData

app.post('/api/inputData',(req,res) => {
    const InputData = {
        id:req.body.id,
        nodeInput: req.body.nodeInput,
      	alarmCondition:  req.body.alarmCondition,
      	recomendationList: req.body.recomendationList 
    }
console.log("recived Message");
console.log(InputData);
InputData.alarmCondition = "rohit";
    cources.push(InputData);
	
	sleep(5000, function() {
	   // executes after one second, and blocks the thread
	   res.send(InputData);
	});
    
});
function sleep(time, callback) {
    var stop = new Date().getTime();
    while(new Date().getTime() < stop + time) {
        ;
    }
    callback();
}

//~~~~~initilizing the port and listening on it~~~~~
const port = process.env.PORT || 3004;

app.listen(port,()=>console.log(`listenning on ${port} port`));
