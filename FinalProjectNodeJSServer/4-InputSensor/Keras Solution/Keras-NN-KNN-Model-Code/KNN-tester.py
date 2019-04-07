

import numpy as np
import pandas as pd
from collections import Counter
print("Hello")

# Get the Last_hidden_Layer_output
train = pd.read_csv("../DataSet/training.csv")
Last_hidden_Layer_output_Training = np.load("../Resource/Last_hidden_Layer_output_Training.npy")
X_train = Last_hidden_Layer_output_Training
a = train.alarm

#TEST DATASET
test = pd.read_csv("../DataSet/test.csv")
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
    print("--")
    # make a list of the k neighbors' targets
    for i in range(k):
        index = distances[i][1]
        #print(y_train)
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

kNearestNeighbor(X_train, a, X_test, predictions, 5)
print ("predictions = ",predictions)
print("---------")
print("final_pred = ",final_pred)
#predictions = np.asarray(predictions)

# evaluating accuracy
#accuracy = accuracy_score(test.alarm, predictions) * 100
#print('\nThe accuracy of classifier is %d%%' % accuracy)
