# Import the needed libraries
import numpy as np
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer  
import pandas as pd  
import tensorflow as tf  
from collections import Counter

import sys
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5_id = sys.argv[5]
#TEST DATASET
#test = pd.read_csv("../DataSet/Test_100/test1Row.csv")
test = pd.read_csv("../DataSet/test1Row.csv")
lables = test.columns.values
alarm = lables[-1]

newXtest = pd.DataFrame([[arg1,arg2,arg3,arg4,0]], columns=lables)
test = test.append(newXtest, ignore_index=True)



testing_data_length = len(test)
Xtest = test.drop(lables[-1], axis=1)
ytest = pd.get_dummies(test.iloc[:,-1])


#print (ytest)

#Input parameter for Neural Network
input_neurons = lables.size-1
output_neuron = ytest.columns.values.size
neuron_per_hiden_layer = [10]
num_hidden_layer = len(neuron_per_hiden_layer)
num_iters = 1000
weights= []
learning_rate = 0.005


# Prediction Model of a created neural network
def prediction_model(input_neurons, Xtest, ytest, num_hidden_layer,trained_weights):
    # Placeholders for input and output data   
    testing_data_length = len(Xtest)
    X = tf.placeholder(shape=(testing_data_length, input_neurons), dtype=tf.float64, name='X')
    y = tf.placeholder(shape=(testing_data_length, output_neuron), dtype=tf.float64, name='y')
    Last_hidden_Layer_output = []

    # Load the Weights
    #trained_weights = np.load("../Resource/Weights.npy")
    # Create the neural net graph    
    A1 = tf.sigmoid(tf.matmul(X, trained_weights[0]))
    for i in range(1,num_hidden_layer+1):
        Last_layer_output = A1
        A1 = tf.sigmoid(tf.matmul(A1, trained_weights[i]))

    # Calculate the predicted outputs
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        predication_result = sess.run(A1, feed_dict={X:Xtest, y:ytest})
        Last_hidden_Layer_output = sess.run(Last_layer_output, feed_dict={X:Xtest, y:ytest})
    return predication_result, Last_hidden_Layer_output



#~~Load the numpy weights of neural network network 
trained_weights = np.load("../Resource/Weights.npy")


#print("----------Testing Data-----")
#~~~ call the predection model for the testing datasert
predication_result,Last_hidden_Layer_output = prediction_model(input_neurons, Xtest, ytest, num_hidden_layer,trained_weights)
#print(np.around(predication_result,3))
##print("---------------")
##print(Last_hidden_Layer_output)
np.save("../Resource/Last_hidden_Layer_output_Testing", Last_hidden_Layer_output)


####################################~~KNN~~################################################


#print("-----------Start KNN------------")

# Get the Last_hidden_Layer_output
train = pd.read_csv("../DataSet/trainingWithSolution.csv")
Last_hidden_Layer_output_Training = np.load("../Resource/Last_hidden_Layer_output_Training.npy")
X_train = Last_hidden_Layer_output_Training
a = train.alarm

#TEST DATASET
X_test = np.load("../Resource/Last_hidden_Layer_output_Testing.npy")


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
##print("X_Train = ",X_train)
kNearestNeighbor(X_train, a, X_test, predictions, 5)

#print("---------")
#print("final_pred = ",final_pred)
#print(np.around(predication_result,3)[2])
winningClass=1
alarmCondition = "NO"

#print("typoe=",type(predication_result[2][0]))

if predication_result[2][0] > predication_result[2][1]:
    winningClass =0

else:
    winningClass =1
    alarmCondition = "YES"

##print("winningClass = ",winningClass," alarmCondition = ",alarmCondition)


trainSolutions = pd.read_csv("../DataSet/trainingWithSolution.csv")
#np_trainSolutions = trainSolutions.values
##print(np_trainSolutions[0][5] )
##print(trainSolutions.at[final_pred[2][0],'solution'])



#########~~~~~~JSON Creation~~~~~~~~~#######

print({
	"id": str(arg5_id),
	"nodeInput": [float(arg1), float(arg2), float(arg3), float(arg4)],
	"alarmCondition": alarmCondition,
	"recomendationList": [
	{
		"resultID": "1",
		"databaseID":str(final_pred[2][0]),
		"result": str(trainSolutions.at[final_pred[2][0],'solution'])
	}, {
		"resultID": "2",
		"databaseID":str(final_pred[2][1]),
		"result": str(trainSolutions.at[final_pred[2][1],'solution'])
	}, {
		"resultID": "3",
		"databaseID":str(final_pred[2][2]),
		"result": str(trainSolutions.at[final_pred[2][2],'solution'])
	}, {
		"resultID": "4",
		"databaseID":str(final_pred[2][3]),
		"result": str(trainSolutions.at[final_pred[2][3],'solution'])
	}, {
		"resultID": "5",
		"databaseID":str(final_pred[2][4]),
		"result": str(trainSolutions.at[final_pred[2][4],'solution'])
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

