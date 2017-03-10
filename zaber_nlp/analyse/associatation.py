#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'zaber'
__time__ = '2017/3/6'

"""
import ahocorasick
import esm
import time

import numpy as np

from .._compat import *


class Association(object):
    def __init__(self):
        self.DEFAULT_ENTITY_NAME = "entity.txt"
        self.DEFAULT_ENTITY = None
        self.ent_list = self.get_entity(self.get_entity_file())
        self.auto = ahocorasick.Automaton()
        self.index = esm.Index()
        self.initialized = False

    def initialize(self):
        start = time.time()
        print "所用实体名称库数据量：", len(self.ent_list)
        int_dict = {}
        for row_idx, int_line in enumerate(self.ent_list):
            for col_idx, v in enumerate(int_line):
                if v in int_dict:
                    int_dict[v].append(str(row_idx) + '.' + str(col_idx))
                else:
                    int_dict[v] = [str(row_idx) + '.' + str(col_idx)]
        for k, v in int_dict.items():
            self.auto.add_word(k, (v, k))
        self.auto.make_automaton()
        print "pyahocorasick加载所用时间：", time.time() - start
        start = time.time()
        for row_idx, int_line in enumerate(self.ent_list):
            for col_idx, v in enumerate(int_line):
                self.index.enter(v, (str(row_idx) + '.' + str(col_idx), v))
        self.index.fix()
        print "esmre加载所用时间：", time.time() - start
        self.initialized = True

    def check_initialized(self):
        # 是否已经加载词库
        if not self.initialized:
            self.initialize()

    def get_entity(self, f):
        ent_list = []
        self.DEFAULT_ENTITY_NAME = resolve_filename(f)
        for index, line in enumerate(f, 1):
            try:
                line = line.strip()
                if line != '':
                    line_list = line.split(' ')
                    ent_list.append(line_list)
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (self.DEFAULT_ENTITY_NAME, index, line))
        f.close()
        return ent_list

    def get_entity_file(self):
        if self.DEFAULT_ENTITY is None:
            return get_module_res(self.DEFAULT_ENTITY_NAME)

    def match_pyahocorasick(self, text):
        self.check_initialized()
        ent_score = np.zeros(len(self.ent_list))
        for find, int_tuple in self.auto.iter(text):
            for idx_item in int_tuple[0]:
                idx = str(idx_item).split('.')
                index = int(idx[0])
                ent_score[index] += 1
        ent_score = np.column_stack((ent_score, self.ent_list))
        ent_sort = sorted(ent_score, key=lambda lamb: lamb[0], reverse=True)
        return ent_sort[:10]

    def match_esmre(self, text):
        self.check_initialized()
        ent_score = np.zeros(len(self.ent_list))
        for find, int_tuple in self.index.query(text):
            idx = str(int_tuple[0]).split('.')
            index = int(idx[0])
            ent_score[index] += 1
        ent_score = np.column_stack((ent_score, self.ent_list))
        ent_sort = sorted(ent_score, key=lambda lamb: lamb[0], reverse=True)
        return ent_sort[:10]

    str_pyahocorasick = match_pyahocorasick
    str_esmre = match_esmre
