# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import pickle
import tensorflow as tf
import numpy as np
from corpus_handel import load_data_and_labels
import json
import pickle
import os
import time
import ahocorasick


class Classify():
    def __init__(self):
        session_conf = tf.ConfigProto(log_device_placement=True, device_count={'GPU': 0})
        self.sess = sess = tf.InteractiveSession(config=session_conf)
        # self.sess=sess = tf.InteractiveSession(device_count = {'GPU': 0})
        # with tf.device('/cpu:0'):
        x = tf.Variable([1.0, 2.0])
        a = tf.constant([3.0, 3.0])
        with sess.as_default():
            # Initialize 'x' using the run() method of its initializer op.
            x.initializer.run()

            # Add an op to subtract 'a' from 'x'.  Run it and print the result
            self.sub = tf.add(x, a)

    def clf(self, word):
        # with tf.device('/cpu:0'):
        with self.sess.as_default():
            print 'xxxxxxxxxxxxxxxxxxx'
            return self.sub.eval()


if __name__ == '__main__':
    a = Classify()
    print a.clf('呵呵呵呵')
