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

  
#fields=['temp1','temp2','pressure1','proximity1','alarm','solution']
fields=[str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6)]
with open(r'../DataSet/trainingWithSolution.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

###~~~~~Send result as print json 

print({
	"result": "Success"
})
sys.stdout.flush()
