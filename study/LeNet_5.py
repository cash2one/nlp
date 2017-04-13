#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'zaber'
__mtime__ = '2017/4/12'

"""
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import SGD

model = Sequential()

# Conv Layer1:
#      w and b init strategy: glorot_uniform
#      w or b regularizer: None
#      activation: None
model.add(Convolution2D(16, 5, 5, border_mode='valid', input_shape=(28, 28, 1)))
model.add(Activation('tanh'))
# Pooling Layer:
#       border_mode: 'valid'
#       strides:  None
model.add(MaxPooling2D((2, 2), border_mode='valid'))

# Conv Layer2:
model.add(Convolution2D(16, 5, 5, border_mode='valid'))
model.add(Activation('tanh'))
model.add(MaxPooling2D((2, 2), border_mode='valid'))

# Flatten the output of MaxPooling_2
# (4,4,16)  ----->  (None,256)
model.add(Flatten())

# full connected layer1:
# 256 cells in flatten layer --- 120 cells in Dense layer
model.add(Dense(120))
model.add(Activation('tanh'))
model.add(Dense(84))
model.add(Activation('tanh'))
model.add(Dense(10))
model.add(Activation('softmax'))
# print the structure of the model
model.summary()

# compile
# loss function: 'mse'
# optimizer_strategy: 'rmsprop'
model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])

# load mnist data
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
X_train = mnist.train.images.reshape((-1, 28, 28, 1))
Y_train = mnist.train.labels
X_test = mnist.test.images.reshape((-1, 28, 28, 1))
Y_test = mnist.test.labels

# train the model
model.fit(X_train, Y_train)

# test the model
model.evaluate(X_test, Y_test)
