import sys
import csv
import numpy as np
import pandas as pd  
import tensorflow as tf  
from collections import Counter

data = np.load("../Resource/Last_hidden_Layer_output_Testing.npy")
training = np.load("../Resource/Last_hidden_Layer_output_Training.npy")
#print(training)

newrow = data[2]
#print(newrow)
print(training.shape)
training = np.vstack([training, newrow])


#np.save("../Resource/Last_hidden_Layer_output_Training.npy",training)

training = np.load("../Resource/Last_hidden_Layer_output_Training.npy")
print(training.shape)
