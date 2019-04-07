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

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5 = sys.argv[5]
arg6 = sys.argv[6]
  
#fields_lables=['temp1','temp2','pressure1','proximity1','alarm','solution']
fields=[str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6)]

train = pd.read_csv("../Keras-DataSet/trainingWithSolution.csv")
df = pd.DataFrame(train)

##~~~~ Adding the row at top
df.loc[-1] = fields
df.index = df.index+1
df = df.sort_index()  # sorting by index
df.to_csv("../Keras-DataSet/trainingWithSolution.csv", sep=',', index=False)


###~~~~~~ Adding new Dataset to last_Hidden_layer_Training.np file
## add the new inputs last hidden layer output to the resource file  

input_test_data = np.array([[arg1,arg2,arg3,arg4]])

from keras.models import load_model
model = load_model("../Keras-Resource/Trained_model")


# Get the last-hidden-layer-output 
inp = model.input                                           # input placeholder
outputs = [layer.output for layer in model.layers]          # all layer outputs
functors = [K.function([inp, K.learning_phase()], [out]) for out in outputs]    # evaluation functions

## Testing get the last hidden layer output
layer_outs = [func([input_test_data, 1.]) for func in functors]
last_hidden_layer_output = layer_outs[1]

## Insert the last hidden layer output to the training set
training = np.load("../Keras-Resource/Last_hidden_Layer_output_Training.npy")
#print(last_hidden_layer_output[0])
newrow = last_hidden_layer_output[0]

training = np.insert(training, 0, newrow, axis=0)
np.save("../Keras-Resource/Last_hidden_Layer_output_Training.npy",training)


###~~~~~Send result as print json

print({
	"result": "Success"
})
sys.stdout.flush()