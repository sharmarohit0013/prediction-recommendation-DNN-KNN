
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


# fix random seed for reproducibility
#np.random.seed(7)
from keras.models import Sequential
from keras.layers import Dense

## read the files 
train = pd.read_csv("../Keras-DataSet/trainingWithSolution.csv")
input_file_incorrect_recommendation = pd.read_csv("../Keras-DataSet/newRecommendationForIncorrectSolution.csv")

## Append the recommendated solution to training dataset
train = train.append(input_file_incorrect_recommendation,ignore_index=True, sort=False)
trained_saved = train ## doing this as solution will get droped and we need solution column for saving the file 
train = train.drop("solution", axis=1) 
dataset = train.values
# load dataset
#dataset = np.loadtxt("../Keras-DataSet/trainingWithSolution.csv", delimiter=",",skiprows = 0)
# remove the first row of features names and split into input (X) and output (Y) variables 
X = dataset[1:,0:4]
Y = dataset[1:,4]


# create model
## 4 input - 2 hidden layer(12,8) - 1 output
model = Sequential()
model.add(Dense(12, input_dim=4, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# Fit the model
model.fit(X, Y, epochs=10, batch_size=3000,verbose=0)


# evaluate the model
scores = model.evaluate(X, Y,verbose=0)
#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


# Get the last-hidden-layer-output 
inp = model.input                                           # input placeholder
outputs = [layer.output for layer in model.layers]          # all layer outputs
functors = [K.function([inp, K.learning_phase()], [out]) for out in outputs]    # evaluation functions

## Testing
layer_outs = [func([X, 1.]) for func in functors]
#print (layer_outs[1])
last_hidden_layer_output = layer_outs[1][0]


# save the weight of the model
#model.save_weights('../Keras-Resource/my_model_weights.h5')

# save the result of the last hidden layer in an .npy file for KNN to use 
np.save("../Keras-Resource/Last_hidden_Layer_output_Training", last_hidden_layer_output)

# save the model which have all the arch and weight
model.save("../Keras-Resource/Trained_model")


#~~~ update the dataset and empty the newRecommendationForIncorrectSolution.csv 
trained_saved.to_csv("../Keras-DataSet/trainingWithSolution.csv",index = False)
## Drop all the entries from dataframe 
input_file_incorrect_recommendation = input_file_incorrect_recommendation.iloc[0:0]
input_file_incorrect_recommendation.to_csv("../Keras-DataSet/newRecommendationForIncorrectSolution.csv",index = False)

###~~~~~Send result as print json
print({
	"result": "Success"
})
sys.stdout.flush()