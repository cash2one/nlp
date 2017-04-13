# coding=utf-8  
import sys, os, json, time

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

from set_logger import set_logger
import logging, traceback

from bfd.harpc import server
from bfd.harpc.common import config
from gen.sentiment.SentimentService import Processor

from senti import Classify


# main service of the thrift api
class SentimentServiceServer(object):
    def __init__(self):
        self.classify = Classify()

    def get_sentiment(self, word, mode='clf'):
        print word, mode
        func = "get_sentiment"
        res = ""
        try:
            if mode == 'clf':
                res = self.classify.clf(word)
            else:
                res = self.clasify.clf3(word)
            print 'res=', res
            logging.info("func: %s \t result: %s ", func, res)

            s_res = json.dumps(res)
            return s_res
        except Exception as e:
            logging.error("error in func: %s !", func)
            traceback.print_exc()
            return json.dumps({})

    def get_opinion_sentence(self, text, ratio=0.5):
        try:
            rval = self.classify.get_opinion_sentence(text, ratio=ratio)
            rval = json.dumps(rval)
            return json.dumps(rval, ensure_asii=False)
        except Exception as e:
            logging.error("error" + str(e))
            return json.dumps('')


def usage():
    print "Usage:"
    print "python sentiment_server.py port processNum."


def setLogger():
    filename = "logs/server.log"
    return set_logger(filename)


if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/server.conf.' + branch
    conf = config.Config(conf_path)
    server_demo = server.GeventProcessPoolThriftServer(Processor, SentimentServiceServer(), conf)
    server_demo.set_post_fork_callback(setLogger)
    print "Starting similar server..."
    server_demo.start()
