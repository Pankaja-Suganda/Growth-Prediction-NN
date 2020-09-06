import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


Data_ = pd.read_csv('Plant Growth Research/Plant_Growth_Data.csv')
Data = Data_.sample(frac=1, replace=True, random_state=1) #One frac = 1440 points
X = np.array(Data[['Group','Day']].values)
Y = np.array(Data[['Height']].values)

GdataX = np.array(Data_['Day'].values).reshape(5,8,36)
GdataY = np.array(Data_['Height'].values).reshape(5,8,36)



def Graph_Subplot(dataX,dataY,Xpred,group):
    color = np.array(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r'])
    plt.figure()
    for i in range(0,8):
        plt.plot(dataX[i], dataY[i], color[i], label='Plant_0' + str(i))

    YPred = np.array([])
    for i in Xpred[group-1][0]:
        YPred = np.append(YPred,sess.run(output,feed_dict={x: i}))
    plt.plot(dataX[0], YPred, color[0], linestyle='-.', linewidth=3,label='Neural Nework Prediction' )
    plt.title('Group 0'+ str(group))
    plt.xlabel('Days')
    plt.ylabel('Height')
    plt.legend(loc='upper left')  
    plt.show()

    return YPred

def Predicted_Graph(dataX,dataY):
    color = np.array(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r'])
    plt.figure()
    for i in range(0,5):
        plt.plot(dataX, dataY[i], color[i], label='Group_0' + str(i+1))
    plt.title('Predicted')
    plt.xlabel('Days')
    plt.ylabel('Height')
    plt.legend(loc='upper left')  
    plt.show()

#X Reshape from (1440,2) to (1440,2,1)
X = X.reshape(1440,2,1)
# X = X/100
Y = Y.reshape(1440,1,1)
# Y = Y/100
#Test Data Arranging
rand = []
test_x_data = []
test_y_data = []

for i in range(0,10):
    val = random.randint(1,1440)
    rand.append(val)
    test_x_data.append(X[val].tolist())
    test_y_data.append(Y[val].tolist())

test_x_data = np.array(test_x_data)
test_y_data = np.array(test_y_data)

# print (rand)
# print (test_x_data)
# print (test_y_data)

# Placeholders for input and output
tf.compat.v1.disable_eager_execution() 
x = tf.compat.v1.placeholder(tf.float32, shape=[2,1])
y = tf.compat.v1.placeholder(tf.float32, shape=[1,1])

# W matrix
W1 = tf.Variable([[1.0,0.0], [1.0, 0.0]], shape=[2,2], name="W1")
W2 = tf.Variable([[0.0] , [1.0]], shape=[2,1], name ="W1")

# Biases
B1 = tf.Variable([[0.0], [0.0]], shape=[2,1], name = "B1")
B2 = tf.Variable([0.0], shape=1, name = "B2")

# Hidden layer and outout layer
output =tf.nn.relu(tf.matmul(tf.nn.relu(tf.matmul(W1, x) + B1), W2, transpose_a =True) + B2)

# error estimation
e = tf.reduce_mean(tf.math.squared_difference(y, output))
train = tf.compat.v1.train.ProximalAdagradOptimizer(0.8).minimize(e)

init = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.Session()
sess.run(init)

print (rand)
print (test_x_data.tolist())
print (test_y_data.tolist())

for i in range(1001):
    for j in range(0,1440):
        j = random.randint(0,1440-1)
        if Y[j] != 0:
            sess.run(train, feed_dict={x: X[j], y: Y[j]})
            sess.run(e, feed_dict={x: X[j], y: Y[j]})
    if i % 100 == 0:
        print('\nEpoch: ' + str(i))
        print('\nError: ' + str(sess.run(e, feed_dict={x: test_x_data[0], y: test_y_data[0]})))
        
        print (rand)
        print (test_x_data.tolist())
        print (test_y_data.tolist())

        for k in range(0,len(test_x_data)):
            print (sess.run(output,feed_dict={x: test_x_data[k]}))



PredictedY = np.array([])
XPred = np.array(Data_[['Group','Day']].values).reshape(5,8,36,2,1)
for i in range(0,5):
    PredictedY = np.append(PredictedY, Graph_Subplot(GdataX[i],GdataY[i],XPred,i+1))
sess.close()
PredictedY = PredictedY.reshape(5,36)
Predicted_Graph(GdataX[0][1], PredictedY)
print ("Complete")

