import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np
import matplotlib.pyplot as plt

x_train = []
y_train = []
x_eval  = []
y_eval  = []

for i in range(100):
    x = np.random.uniform(0,3)
    y = np.exp(np.sin(x))**0.3 +1
    if i%2==0:
        x_train.append(x)
        y_train.append(y)
    else:
        x_eval.append(x)
        y_eval.append(y)

x_train_arr = np.array(x_train)
y_train_arr = np.array(y_train)
x_eval_arr = np.array(x_eval)
y_eval_arr = np.array(y_eval)

plt.plot(x_train, y_train, 'ro')
print(x_train,y_train)
#plt.axis([0, 6, 0, 20])
plt.show()


import tensorflow as tf
# NumPy is often used to load, manipulate and preprocess data.

# Declare list of features. We only have one numeric feature. There are many
# other types of columns that are more complicated and useful.
feature_columns = [tf.feature_column.numeric_column("x", shape=[1])]

# An estimator is the front end to invoke training (fitting) and evaluation
# (inference). There are many predefined types like linear regression,
# linear classification, and many neural network classifiers and regressors.
# The following code provides an estimator that does linear regression.
estimator = tf.estimator.LinearRegressor(feature_columns=feature_columns)

# TensorFlow provides many helper methods to read and set up data sets.
# Here we use two data sets: one for training and one for evaluation
# We have to tell the function how many batches
# of data (num_epochs) we want and how big each batch should be.
#x_train = np.array([1., 2., 3., 4.])
#y_train = np.array([0., -1., -2., -3.])
#x_eval = np.array([2., 5., 8., 1.])
#y_eval = np.array([-1.01, -4.1, -7, 0.])
input_fn = tf.estimator.inputs.numpy_input_fn(
    {"x": x_train_arr}, y_train_arr, batch_size=4, num_epochs=None, shuffle=True)
train_input_fn = tf.estimator.inputs.numpy_input_fn(
    {"x": x_train_arr}, y_train_arr, batch_size=4, num_epochs=1000, shuffle=False)
eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    {"x": x_eval_arr}, y_eval_arr, batch_size=4, num_epochs=1000, shuffle=False)

# We can invoke 1000 training steps by invoking the  method and passing the
# training data set.
estimator.train(input_fn=input_fn, steps=1000)

# Here we evaluate how well our model did.
train_metrics = estimator.evaluate(input_fn=train_input_fn)
eval_metrics = estimator.evaluate(input_fn=eval_input_fn)
print("train metrics: %r"% train_metrics)
print("eval metrics: %r"% eval_metrics)

