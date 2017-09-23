from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import urllib.request as urllib

import numpy as np
import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Data sets

#IRIS_TRAINING = "iris_training.csv"
#IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"

#IRIS_TEST = "iris_test.csv"
#IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

def main():
  test_training = "data.csv"
  test_evaluation = "data.csv"
#  # If the training and test sets aren't stored locally, download them.
#  if not os.path.exists(IRIS_TRAINING):
#    raw = urllib.urlopen(IRIS_TRAINING_URL).read()
#    with open(IRIS_TRAINING, "wb") as f:
#      f.write((raw))
    
#  if not os.path.exists(IRIS_TEST):
#    raw = urllib.urlopen(IRIS_TEST_URL).read()
#    with open(IRIS_TEST, "wb") as f:
#      f.write((raw))
  
  # Load datasets.
  training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
      filename=test_training,
      target_dtype=np.float32,
      features_dtype=np.int)
  test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
      filename=test_evaluation,
      target_dtype=np.float32,
      features_dtype=np.int)

  # Specify that all features have real-value data
  feature_columns = [tf.feature_column.numeric_column("x", shape=[3])]

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  regressor = tf.estimator.DNNRegressor(feature_columns=feature_columns,
                                          hidden_units=[10, 20, 10],
#                                          model_dir="/tmp/iris_model"
                                          )
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(training_set.data)},
      y=np.array(training_set.target),
      num_epochs=None,
      shuffle=True)

  # Train model.
  regressor.train(input_fn=train_input_fn, steps=2000)

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(test_set.data)},
      y=np.array(test_set.target),
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  ev = regressor.evaluate(input_fn=test_input_fn, steps=1)
  loss_score = ev["loss"]
  print("Loss: {0:f}".format(loss_score))


#  print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

  # Classify two new flower samples.
#28,2,0,1
#28,11,6,0
#28,1,8,3
#28,7,10,1
#28,15,12,22
#28,3,17,0
#28,5,19,0
#28,9,18,2
#28,16,4,0
  
  new_samples = np.array([
    [28,2,0],
    [28,11,6],
    [28,1,8],
    [28,7,10],
    [28,15,12],
    [28,3,17],
    [28,5,19],
    [28,9,18],
    [28,16,4],
  ], dtype=np.int)
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": new_samples},
      num_epochs=1,
      shuffle=False)

  predictions = list(regressor.predict(input_fn=predict_input_fn))
  predicted_classes = [p["predictions"] for p in predictions]

  for i in range(len(new_samples)):
    print(new_samples[i][0],new_samples[i][1],new_samples[i][2],'\t',predicted_classes[i])
  print(
      "New Samples, Predictions:    {}\n"
      .format(predicted_classes))

if __name__ == "__main__":
    main()

