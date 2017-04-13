# encoding=utf-8
# !/usr/bin/env python
import json
import sys, os
from set_logger import set_logger
import socket
import logging
import time

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

from bfd.harpc import server
from bfd.harpc.common import config
from gen.segment.SegmentService import Processor

from segment import Segment


class SegmentHander(object):
    def __init__(self):
        self.seg = None

    def get_pos_tag(self, word, user_dicts):
        res = ""
        self.seg = Segment("pos_map.txt", user_dict_path=user_dicts)
        try:
            res = self.seg.pos_seg(word)
            res = json.dumps(res, ensure_ascii=False)
            logging.info(res)
        except Exception, e:
            logging.error(e)
        return res

    def get_ner(self, word):
        res = ""
        try:
            res = self.seg.ner_recog(word)
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
    server_demo = server.GeventProcessPoolThriftServer(Processor, SegmentHander(), conf)
    server_demo.set_post_fork_callback(setLogger)
    print "Starting chinese segment server..."
    server_demo.start()
