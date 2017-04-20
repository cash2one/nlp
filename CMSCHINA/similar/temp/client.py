#encoding=utf-8
import json
#import readline
from gen.similar.SimilarService import Client
from bfd.harpc.common import config
from bfd.harpc import client
import sys

        

if __name__ == '__main__':
    branch=sys.argv[1]
    conf_path='etc/client.conf.'+branch
    conf = config.Config(conf_path)
    manager = client.Client(Client,conf)
    client_ = manager.create_proxy()
    
    # 同义词只有一种格式，输入一个词，返回一个LIST
    word=json.dumps('习近平')
    

    # 近义词可以指定参数
    words=['习近平','政治','毛泽东','保税物流中心_(A型)']
    modes1=['auto','only_extended','auto_split']
    modes2=['auto','auto_split','tyccl+wiki+split','word2vec+split']

    def process(word):
        for mode in modes1:
            print 'synonym'
            print 'word=',word
            word2=json.dumps(word)
            print 'mode=',mode
            print 'result=',client_.synonym(word2,mode),'\n'

        for mode in modes2:
            print 'nearsynonym'
            print 'word=',word
            word2=json.dumps(word)
            print 'mode=',mode
            print 'result=',client_.nearsynonym(word2,50,mode),'\n'
    
    for word in words:
        process(word)

    while True:
        word=raw_input('Enter word')
        process(word)
    
