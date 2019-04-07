# Import the needed libraries
import numpy as np
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer  
import pandas as pd  
import tensorflow as tf  
from collections import Counter

print("hello")

#TEST DATASET
#test = pd.read_csv("../DataSet/Test_100/test1Row.csv")
test = pd.read_csv("../DataSet/test1Row.csv")
lables = test.columns.values
alarm = lables[-1]

newXtest = pd.DataFrame([[5,3,1.6,0.2,0]], columns=lables)
test = test.append(newXtest, ignore_index=True)



testing_data_length = len(test)
Xtest = test.drop(lables[-1], axis=1)
ytest = pd.get_dummies(test.iloc[:,-1])


print (ytest)

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


print("----------Testing Data-----")
#~~~ call the predection model for the testing datasert
predication_result,Last_hidden_Layer_output = prediction_model(input_neurons, Xtest, ytest, num_hidden_layer,trained_weights)
print(np.around(predication_result,3))
#print("---------------")
print("Last_hidden_Layer_output =",Last_hidden_Layer_output)
np.save("../Resource/Last_hidden_Layer_output_Testing", Last_hidden_Layer_output)
