# -*- coding: utf-8 -*-

import zaber_nlp.analyse

content = open("../study/origin/aa", "rb").read()
zaber_nlp.analyse.Associate_find(content)
zaber_nlp.analyse.Associate(content)
