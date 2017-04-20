# encoding=utf-8
#!/usr/bin/env python
from argparse import ArgumentParser
import json
import sys,os
from set_logger import set_logger
import socket
import logging
import time


cur_dir = os.path.dirname( os.path.abspath(__file__)) or os.getcwd()
'''
sys.path.append(cur_dir)
sys.path.append(cur_dir + '/similar')
'''

from bfd.harpc import server
from bfd.harpc.common import config
from gen.similar.SimilarService import Processor

from similar.similar import Model 

# analyzer_version='object-12-06'

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
 
class SimilarHander(object):
    def __init__(self):
        self.model=Model(
            cur_dir+'/similar/synonym.txt', 
            cur_dir+'/similar/tyccl.txt', 
            cur_dir+'/similar/redirect.txt', 
            cur_dir+'/similar/wiki_similar.txt',
            cur_dir+'/similar/vec.txt')
    
    def synonym(self, word, mode):#TODO:如果输入多个词，就返回他们的共同同义词
        word=byteify(json.loads(word))
        try:
            rval=self.model.synonym(word,mode)
            rval=json.dumps(rval,ensure_ascii=False)
            logging.info('Successful:'+word)
        except Exception,e:
            rval=[]
            rval=json.dumps(rval,ensure_ascii=False)
            logging.error('Error:'+word+'\t'+str(e))
        return rval

    def nearsynonym(self, word, topn, mode):
        word=byteify(json.loads(word))
        try:
            rval=self.model.nearsynonym(word, topn, mode)
            rval=json.dumps(rval,ensure_ascii=False)
            logging.info('Successful:'+word)
        except Exception,e:
            rval=[]
            rval=json.dumps(rval,ensure_ascii=False)
            logging.error('Error:'+word+'\t'+str(e))
        return rval
         
def setLogger():
    filename = "logs/server.log"
    return set_logger(filename)

if __name__=='__main__':
    branch=sys.argv[1]
    conf_path='etc/server.conf.'+branch
    conf = config.Config(conf_path)
    server_demo = server.GeventProcessPoolThriftServer(Processor,SimilarHander(), conf)
    server_demo.set_post_fork_callback(setLogger)
    print "Starting similar server..."
    server_demo.start()

