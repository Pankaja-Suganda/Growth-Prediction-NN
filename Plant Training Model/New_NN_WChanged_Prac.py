import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# input X vector
X = [[[0.0], [0.0]], [[0.0],[1.0]], [[1.0], [0.0]], [[1.0], [1.0]]]
# output Y vector
Y = [[[0.0]], [[1.0]], [[1.0]], [[0.0]]]

# Data = pd.read_csv('Plant Growth Research/Plant_Growth_Data.csv')
# Data = Data.sample(frac=2, replace=True, random_state=1)
# x_data = np.array(Data[['Day']].values)
# y_data = np.array(Data[['Height']].values)

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
# activation function is Sigmoid (0,1)
output =tf.sigmoid(tf.matmul(tf.sigmoid(tf.matmul(W1, x) + B1), W2, transpose_a =True) + B2)
 
# error estimation

e = tf.reduce_mean(tf.math.squared_difference(y, output))
train = tf.compat.v1.train.GradientDescentOptimizer(0.5).minimize(e)

init = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.Session()
sess.run(init)


for i in range (1001):
    for k in range(0,4):
        j = random.randint(0,3)
        sess.run(train, feed_dict={x: X[j], y: Y[j]})
        sess.run(e, feed_dict={x: X[j], y: Y[j]})
    if i % 1000 == 0:
        print('\nEpoch: ' + str(i))
        for k in range(0,4):
            print('\nError: ' + str(sess.run(e, feed_dict={x: X[k], y: Y[k]})))
        
        for k in range(0,4):
            print (sess.run(output,feed_dict={x: X[k]}))


# for i in range(25):
#     for j in range(25):
#         x_data = np.array([[i/25],[j/25]])
#         answer = sess.run(output,feed_dict={x: x_data})
#         plt.scatter(i/25,j/25, c= str(answer[0][0]) )

# plt.show()
        
sess.close()
print ("Complete")

