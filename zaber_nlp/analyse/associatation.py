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
        ent_dict = {}
        ent_list = [[0, []]]
        self.DEFAULT_ENTITY_NAME = resolve_filename(f)
        for index, line in enumerate(f, 1):
            try:
                line = line.strip()
                if line != '':
                    line_list = line.split(' ')
                    for idx, ent in enumerate(line_list):
                        ent_dict[str(index) + '.' + str(idx)] = ent
                    ent_list.append([0, line_list])
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (self.DEFAULT_ENTITY_NAME, index, line))
        f.close()
        return ent_dict, ent_list

    def got_entity(self, f):
        ent_dict = {}
        ent_list = [[0, []]]
        self.DEFAULT_ENTITY_NAME = resolve_filename(f)
        for index, line in enumerate(f, 1):
            try:
                line = line.strip()
                if line != '':
                    line_list = line.split(' ')
                    for idx, ent in enumerate(line_list):
                        ent_dict[ent] = str(index) + '.' + str(idx)
                    ent_list.append([0, line_list])
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (self.DEFAULT_ENTITY_NAME, index, line))
        f.close()
        return ent_dict, ent_list

    def get_entity_file(self):
        if self.DEFAULT_ENTITY is None:
            return get_module_res(self.DEFAULT_ENTITY_NAME)

    def match(self, text):
        start = time.time()
        int_dict, int_list = self.get_entity(self.get_entity_file())
        auto = ahocorasick.Automaton()
        for k, v in int_dict.items():
            auto.add_word(v, (k, v))
        auto.make_automaton()
        for find, int_tuple in auto.iter(text):
            idx = str(int_tuple[0]).split('.')
            index = int(idx[0])
            int_list[index][0] += 1
        int_sort = sorted(int_list, key=lambda lamb: lamb[0], reverse=True)
        print time.time() - start
        print str(int_sort[:10]).decode(encoding='string_escape')
        return int_sort[:10]

    def match_esmre(self, text):
        start = time.time()
        int_dict, int_list = self.get_entity(self.get_entity_file())
        index = esm.Index()
        for v in int_dict.values():
            index.enter(v)
        index.fix()
        print str(index.query(text)).decode(encoding='string_escape')
        for result_tuple in index.query(text):
            print int_dict.keys()[int_dict.values().index(result_tuple[1])]
        int_sort = sorted(int_list, key=lambda lamb: lamb[0], reverse=True)
        print time.time() - start
        return int_sort[:10]

    str_match = match
    str_find = match_esmre
