# Import the needed libraries
import sys
import numpy as np
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer  
import pandas as pd  
import tensorflow as tf  
#print("hello")
train = pd.read_csv("../DataSet/trainingWithSolution.csv")
train = train.drop("solution", axis=1) 

lables = train.columns.values
alarm = lables[-1]
# TRAIN DATASET
Xtrain = train.drop(lables[-1], axis=1)  
# Encode target values into binary ('one-hot' style) representation
ytrain = pd.get_dummies(train.iloc[:,-1])


#Input parameter for Neural Network
input_neurons = lables.size-1
output_neuron = ytrain.columns.values.size
training_data_length = len(train)
neuron_per_hiden_layer = [10]
num_hidden_layer = len(neuron_per_hiden_layer)
num_iters = 3000
weights= []
learning_rate = 0.005


# Create and train a tensorflow model of a neural network
def create_train_model(input_neurons,num_iters):
    # Reset the graph
    tf.reset_default_graph()

    # Placeholders for input and output data
    #X = tf.placeholder(shape=(85, 4), dtype=tf.float64, name='X')
    #y = tf.placeholder(shape=(85, 2), dtype=tf.float64, name='y')
    
    X = tf.placeholder(shape=(training_data_length, input_neurons), dtype=tf.float64, name='X')
    y = tf.placeholder(shape=(training_data_length, output_neuron), dtype=tf.float64, name='y')
    
    #~~~~~Initilization of weights matrix~~~~~~

    #input-Layer to first hidden-layer
    weights.append(tf.Variable(np.random.rand(input_neurons, neuron_per_hiden_layer[0]), dtype=tf.float64))
    #first hidden-layer to last hidden layer
    for x in range(1,num_hidden_layer):
        # hidden-layer x-1 to hidden-layer x
        weights.append(tf.Variable(np.random.rand(neuron_per_hiden_layer[x-1], neuron_per_hiden_layer[x]), dtype=tf.float64))
    #lass hidden-layer to output-;ayer
    weights.append(tf.Variable(np.random.rand(neuron_per_hiden_layer[-1], output_neuron), dtype=tf.float64))
     
    Last_hidden_Layer_output = []
    # Create the neural net graph    
    A1 = tf.sigmoid(tf.matmul(X, weights[0]))
    for i in range(1,num_hidden_layer+1):
        Last_layer_output = A1
        A1 = tf.sigmoid(tf.matmul(A1, weights[i]))

    # Define a loss function
    deltas = tf.square(A1 - y)
    loss = tf.reduce_sum(deltas)

    # Define a train operation to minimize the loss
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train = optimizer.minimize(loss)
   
    # Initialize variables and run session
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    weights_final = []
    # Go through num_iters iterations
    for i in range(num_iters):
        weights_local = []
        sess.run(train,feed_dict={X:Xtrain,y:ytrain})
        Last_hidden_Layer_output = sess.run(Last_layer_output, feed_dict={X:Xtrain,y:ytrain})
        for w in weights:
            weights_local.append(sess.run(w))
        weights_final = weights_local
    #for h in neuron_per_hiden_layer:
    #   #print("loss (hidden nodes: %d, iterations: %d): %.2f"%(h[0], num_iters,loss_plot[h][-1]))
    sess.close()
    return weights_final,Last_hidden_Layer_output

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


trained_weights,Last_hidden_Layer_output= create_train_model(input_neurons, num_iters)
#np.save("../Resource/Last_hidden_Layer_output_Training", Last_hidden_Layer_output)
##print( np.load("../Resource/Last_hidden_Layer_output_Training.npy"))
#for w in trained_weights:
   ##print(w)

np.save("../Resource/Weights", trained_weights)

#~~Load the numpy weights of neural network network 
trained_weights = np.load("../Resource/Weights.npy")


#print("----------Training Data-----")
#~~~ call the predection model for training dataset
predication_result,Last_hidden_Layer_output = prediction_model(input_neurons, Xtrain, ytrain, num_hidden_layer,trained_weights)
#print(np.around(predication_result,3))
#print("---------------")
##print(Last_hidden_Layer_output)
np.save("../Resource/Last_hidden_Layer_output_Training", Last_hidden_Layer_output)


###~~~~~Send result as print json

print({
	"result": "Success"
})
sys.stdout.flush()