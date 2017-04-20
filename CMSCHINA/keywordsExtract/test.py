#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'zaber'
__mtime__ = '2017/4/18'

"""
import os
import sys

import settings

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
from keywords import Keywords
import codecs

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    f = open(input_path, 'rb')
    text = f.read().decode('utf-8')
    f.close()
    topN = 1000
    kw = Keywords(settings.df_file, settings.stopwords)
    d_res = kw.process(text, topN, '')
    file_object = codecs.open(output_path, 'w', "utf-8")
    for k, v in d_res.items()[0:20]:
        file_object.write('关键词： ' + k + ', 权重： ' + str(v) + '\n')
    file_object.close()
