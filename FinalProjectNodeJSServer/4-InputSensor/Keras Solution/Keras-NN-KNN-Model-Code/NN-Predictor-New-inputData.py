import sys
import csv
import numpy as np
import pandas as pd  
import tensorflow as tf  
from collections import Counter

data = np.load("../Keras-Resource/Last_hidden_Layer_output_Testing.npy")
training = np.load("../Keras-Resource/Last_hidden_Layer_output_Training.npy")
print(training)

newrow = data

training = np.load("../Keras-Resource/Last_hidden_Layer_output_Training.npy")
print(training.shape)
#print (training)



# Get the Last_hidden_Layer_output
train = pd.read_csv("../Keras-DataSet/trainingWithSolution.csv")
#print(train['temp1'].idxmax())

