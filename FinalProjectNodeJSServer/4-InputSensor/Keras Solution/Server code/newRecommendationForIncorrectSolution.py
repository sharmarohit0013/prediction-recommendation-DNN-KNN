# Import the needed libraries
import sys
import csv
import numpy as np
import pandas as pd  
import tensorflow as tf  
from collections import Counter

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5 = sys.argv[5]
arg6 = sys.argv[6]

import csv
list1=[arg1,arg2,arg3,arg4,arg5,arg6]

with open("../Keras-DataSet/newRecommendationForIncorrectSolution.csv", "a", newline='') as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerow(list1)


print({
	"result": "Success"
})
sys.stdout.flush()
