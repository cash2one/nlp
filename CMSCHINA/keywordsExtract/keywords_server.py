# encoding=utf-8
# !/usr/bin/env python
import json
import sys, os
from set_logger import set_logger
import socket
import logging
import time
import settings

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

from bfd.harpc import server
from bfd.harpc.common import config
from gen.keywords.KeywordsService import Processor

from keywords import Keywords


class KeywordsHander(object):
    def __init__(self):
        self.kw = Keywords(settings.df_file, settings.stopwords)

    def get_keywords(self, word, topN):
        res = ""
        try:
            res = self.kw.process(word, topN)
            res = json.dumps(res, ensure_ascii=False)
        except Exception, e:
            logging.error(e)
        return res


def setLogger():
    filename = "logs/server.log"
    return set_logger(filename)


if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/server.conf.' + branch
    conf = config.Config(conf_path)
    server_demo = server.GeventProcessPoolThriftServer(Processor, KeywordsHander(), conf)
    server_demo.set_post_fork_callback(setLogger)
    print "Starting keywords server..."
    server_demo.start()
