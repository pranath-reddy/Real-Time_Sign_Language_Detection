# Authors : Pranath Reddy

import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import matplotlib.pyplot as plt
from tensorflow.python.lib.io import file_io
from pandas.compat import StringIO

# import Data
print("Importing the Data")

tdata = pd.read_csv('./test.csv')

xt = tdata.iloc[:,1:].values

yt = tdata.iloc[:,:1].values.flatten()

data = pd.read_csv('./train.csv')

x = data.iloc[:, 1:].values

y = data.iloc[:, :1].values.flatten()

def one_hot_encode(y):
    return np.eye(25)[y]
y_encoded = one_hot_encode(y)

learning_rate = 0.001
batch_size = 128
epochs = 20000
display_step = 500

n_inputs = 784
nh1 = 256
nh2 = 256
nh3 = 256
nh4 = 256
nh5 = 256
n_outputs = 25

X = tf.placeholder('float', [None, n_inputs])
Y = tf.placeholder('float', [None, n_outputs])

# Creating Network, Layers

weights = {
    'w1' : tf.Variable(tf.random_normal([n_inputs, nh1])),
    'w2' : tf.Variable(tf.random_normal([nh1, nh2])),
    'w3' : tf.Variable(tf.random_normal([nh2, nh3])),
    'w4' : tf.Variable(tf.random_normal([nh3, nh4])),
    'w5' : tf.Variable(tf.random_normal([nh4, nh5])),
    'out_w' : tf.Variable(tf.random_normal([nh5, n_outputs]))
}

biases = {
    'b1' : tf.Variable(tf.random_normal([nh1])),
    'b2' : tf.Variable(tf.random_normal([nh2])),
    'b3' : tf.Variable(tf.random_normal([nh3])),
    'b4' : tf.Variable(tf.random_normal([nh4])),
    'b5' : tf.Variable(tf.random_normal([nh5])),
    'out_b' : tf.Variable(tf.random_normal([n_outputs]))
}

def neural_network(x, weights, biases):
    layer1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
    layer2 = tf.add(tf.matmul(layer1, weights['w2']), biases['b2'])
    layer3 = tf.add(tf.matmul(layer2, weights['w3']), biases['b3'])
    layer4 = tf.add(tf.matmul(layer3, weights['w4']), biases['b4'])
    layer5 = tf.add(tf.matmul(layer4, weights['w5']), biases['b5'])
    layer_out = tf.matmul(layer5, weights['out_w']) + biases['out_b']
    return layer_out

logits = neural_network(X, weights, biases)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = logits, labels = Y))

optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate)
training_op = optimizer.minimize(loss_op)

correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

def next_batch(batch_size, data, labels):
    idx = np.arange(0, len(data))
    np.random.shuffle(idx)
    idx = idx[: batch_size]
    data_shuffle = [data[i] for i in idx]
    labels_shuffle = [labels[i] for i in idx]
    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

print("importing the Trained network, ignore any warnings")

# Tf Session

with tf.Session() as sess:
    
    sess.run(init)
    
    saver = tf.train.Saver()
    saver.restore(sess,'./save.ckpt')

    W = sess.run(weights)
    B = sess.run(biases)


# Testing

def neural_network(x, weights, biases):
    layer1 = np.matmul(x, weights['w1']) + biases['b1']
    layer2 = np.matmul(layer1, weights['w2']) + biases['b2']
    layer3 = np.matmul(layer2, weights['w3']) + biases['b3']
    layer4 = np.matmul(layer3, weights['w4']) + biases['b4']
    layer5 = np.matmul(layer4, weights['w5']) + biases['b5']
    layer_out = np.matmul(layer5, weights['out_w']) + biases['out_b']
    return layer_out


def get_predictions(x, w, b):
    pred = neural_network(x, w, b)
    images, predictions = [], []
    for i in x:
        images.append(i.reshape(28, 28))
    for i in pred:
        predictions.append(list(i))
    predictions = [chr(int(i.index(max(i))) + ord('A')) for i in predictions]
    return (images, predictions)


#images, preds = get_predictions(x, W, B)

images2, preds2 = get_predictions(xt, W, B)

plt.imshow(images2[5])
plt.title(preds2[5])
plt.show()