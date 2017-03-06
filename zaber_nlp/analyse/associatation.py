#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'zaber'
__time__ = '2017/3/6'

"""
from .._compat import *

DEFAULT_ENTITY_NAME = "entity.txt"
DEFAULT_ENTITY = None


class Association(object):
    def get_entity(self, f):
        ent_dict = {}  # 字典存储 词条:出现次数
        f_name = resolve_filename(f)
        for lineno, line in enumerate(f, 1):
            try:
                print (lineno, line)
                line = line.strip().decode('utf-8')
                ent_list = line.split(' ')
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (f_name, lineno, line))
        f.close()
        self.get_entity(self.get_entity_file())

    def get_entity_file(self):
        if DEFAULT_ENTITY is None:
            return get_module_res(DEFAULT_ENTITY_NAME)

    def match(self):
        self.get_entity(self.get_entity_file())

    str_match = match
