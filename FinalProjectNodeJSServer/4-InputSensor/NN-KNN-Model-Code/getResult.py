
import sys
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5 = sys.argv[5]


import numpy as np
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer  
import pandas as pd  
import tensorflow as tf  
from collections import Counter

#~~Load the numpy weights of neural network network 
trained_weights = np.load("../Resource/Weights.npy")

print({
	"id": arg5,
	"nodeInput": [1, 2, 3, 4],
	"alarmCondition": "No",
	"recomendationList": [
	{
		"resultID": "1",
		"databaseID":"101",
		"result": " a ROjhhhhit fndsjko; thsis"
	}, {
		"resultID": "2",
		"databaseID":"105",
		"result": " b do this"
	}, {
		"resultID": "3",
		"databaseID":"106",
		"result": " c do this"
	}, {
		"resultID": "4",
		"databaseID":"113",
		"result": " d do this"
	}, {
		"resultID": "5",
		"databaseID":"131",
		"result": " e do this"
	}]
})
sys.stdout.flush()
