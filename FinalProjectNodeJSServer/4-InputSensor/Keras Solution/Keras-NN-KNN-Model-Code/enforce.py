
# Just disables the warning, doesn't enable AVX/FMA
import sys, os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import keras
sys.stderr = stderr

#Suppress messages from tensorflow
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import load_model
sys.stderr = stderr
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Import the needed libraries
import numpy as np
from keras import backend as K
import pandas as pd  
import tensorflow as tf  
from collections import Counter

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5_id = sys.argv[5]

input_test_data = np.array([[arg1,arg2,arg3,arg4]])

from keras.models import load_model
model = load_model("../Keras-Resource/Trained_model")


# Predict the result ==> [[1,2,3,4]] ==> [[0.65655]]
predicted_output = model.predict(input_test_data)[0][0]


# Get the last-hidden-layer-output 
inp = model.input                                           # input placeholder
outputs = [layer.output for layer in model.layers]          # all layer outputs
functors = [K.function([inp, K.learning_phase()], [out]) for out in outputs]    # evaluation functions

## Testing
layer_outs = [func([input_test_data, 1.]) for func in functors]

last_hidden_layer_output = layer_outs[1]
#print (last_hidden_layer_output)

np.save("../Keras-Resource/Last_hidden_Layer_output_Testing", last_hidden_layer_output)




####################################~~KNN~~################################################


#print("-----------Start KNN------------")

# Get the Last_hidden_Layer_output
train = pd.read_csv("../Keras-DataSet/trainingWithSolution.csv")
Last_hidden_Layer_output_Training = np.load("../Keras-Resource/Last_hidden_Layer_output_Training.npy")
X_train = Last_hidden_Layer_output_Training

y_train = train.alarm

#TEST DATASET
X_test = np.load("../Keras-Resource/Last_hidden_Layer_output_Testing.npy")


final_pred = []

def predict(X_train, y_train, x_test, k):

    # create list for distances and targets
    distances = []
    targets = []
    for i in range(len(X_train)):
        # first we compute the euclidean distance
        distance = np.sqrt(np.sum(np.square(x_test - X_train[i, :])))
        # add it to list of distances
        distances.append([distance, i])

    # sort the list
    distances = sorted(distances)
    pred_distances = distances[0:k]
    #print(distances[0:3])
    dis = []
    for arr in pred_distances:
        dis.append(arr[1])
    final_pred.append(dis)
    #print("--",final_pred)
    # make a list of the k neighbors' targets
    for i in range(k):
        index = distances[i][1]
        ##print(y_train)
        targets.append(y_train[index])
    # return most common target
    return Counter(targets).most_common(1)[0][0]

def kNearestNeighbor(X_train, y_train, X_test, predictions, k):
	# check if k is not larger than n
	if k > len(X_train):
		raise ValueError
		
	
	# predict for each testing observation
	for i in range(len(X_test)):
		predictions.append(predict(X_train, y_train, X_test[i, :], k))

# ============================== testing our KNN =============================================
# making our predictions 
predictions = []
kNearestNeighbor(X_train, y_train, X_test, predictions, 10)
#print(final_pred)
#print("---")
# Default Parameter
winningClass=1
alarmCondition = "NO"

if predicted_output>0.5:
    winningClass =1
    alarmCondition = "YES"
    

trainSolutions = train

#########~~~~~~JSON Creation~~~~~~~~~#######

print({
	"id": str(arg5_id),
	"nodeInput": [float(arg1), float(arg2), float(arg3), float(arg4)],
	"alarmCondition": alarmCondition,
	"recomendationList": [
	{
		"resultID": "1",
		"databaseID":str(final_pred[0][0]),
		"result": str(trainSolutions.at[final_pred[0][0],'solution'])
	}, {
		"resultID": "2",
		"databaseID":str(final_pred[0][1]),
		"result": str(trainSolutions.at[final_pred[0][1],'solution'])
	}, {
		"resultID": "3",
		"databaseID":str(final_pred[0][2]),
		"result": str(trainSolutions.at[final_pred[0][2],'solution'])
	}, {
		"resultID": "4",
		"databaseID":str(final_pred[0][3]),
		"result": str(trainSolutions.at[final_pred[0][3],'solution'])
	}, {
		"resultID": "5",
		"databaseID":str(final_pred[0][4]),
		"result": str(trainSolutions.at[final_pred[0][4],'solution'])
	}]
})
"""
print({
	"id": arg5_id,
	"nodeInput": [1, 2, 3, 4],
	"alarmCondition": "No",
	"recomendationList": [
	{
		"id": "1",
		"databaseID":"101",
		"result": " a ROjhhhhit fndsjko; thsis"
	}, {
		"id": "2",
		"databaseID":"105",
		"result": " b do this"
	}, {
		"id": "3",
		"databaseID":"106",
		"result": " c do this"
	}, {
		"id": "4",
		"databaseID":"113",
		"result": " d do this"
	}, {
		"id": "5",
		"databaseID":"131",
		"result": " e do this"
	}]
})
"""
sys.stdout.flush()

