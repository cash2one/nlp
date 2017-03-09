#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'zaber'
__time__ = '2017/3/6'

"""
import ahocorasick
import esm
import time

from .._compat import *


class Association(object):
    DEFAULT_ENTITY_NAME = "entity.txt"
    DEFAULT_ENTITY = None

    def get_entity(self, f):
        ent_list = []
        self.DEFAULT_ENTITY_NAME = resolve_filename(f)
        for index, line in enumerate(f, 1):
            try:
                line = line.strip()
                if line != '':
                    line_list = line.split(' ')
                    ent_list.append([0, line_list])
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (self.DEFAULT_ENTITY_NAME, index, line))
        f.close()
        return ent_list

    def get_entity_file(self):
        if self.DEFAULT_ENTITY is None:
            return get_module_res(self.DEFAULT_ENTITY_NAME)

    def match(self, text):
        int_list = self.get_entity(self.get_entity_file())
        start = time.time()
        auto = ahocorasick.Automaton()
        int_dict = {}
        for row_idx, int_line in enumerate(int_list):
            for col_idx, v in enumerate(int_line[1:][0]):
                if v in int_dict:
                    int_dict[v].append(str(row_idx) + '.' + str(col_idx))
                else:
                    int_dict[v] = [str(row_idx) + '.' + str(col_idx)]
        for k, v in int_dict.items():
            auto.add_word(k, (v, k))
        auto.make_automaton()
        print time.time() - start
        for find, int_tuple in auto.iter(text):
            for idx_item in int_tuple[0]:
                idx = str(idx_item).split('.')
                index = int(idx[0])
                int_list[index][0] += 1
        int_sort = sorted(int_list, key=lambda lamb: lamb[0], reverse=True)
        print time.time() - start
        print str(int_sort[:15]).decode(encoding='string_escape')
        return int_sort[:15]

    def match_esmre(self, text):
        int_list = self.get_entity(self.get_entity_file())
        start = time.time()
        index = esm.Index()
        for row_idx, int_line in enumerate(int_list):
            for col_idx, v in enumerate(int_line[1:][0]):
                index.enter(v, (str(row_idx) + '.' + str(col_idx), v))
        index.fix()
        print time.time() - start
        for find, int_tuple in index.query(text):
            idx = str(int_tuple[0]).split('.')
            index = int(idx[0])
            int_list[index][0] += 1
        int_sort = sorted(int_list, key=lambda lamb: lamb[0], reverse=True)
        print time.time() - start
        print str(int_sort[:15]).decode(encoding='string_escape')
        return int_sort[:15]

    str_match = match
    str_find = match_esmre
