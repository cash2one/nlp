# encoding=utf-8
# !flask/bin/python
from flask import request
from flask import Flask, jsonify
from senti import *
from set_logger import set_logger
import logging
import traceback


def setLogger():
    filename = "logs/server.log"
    return set_logger(filename)


senti = Flask(__name__)

model = Classify()
setLogger()
'''
curl -i -H "Content-Type: application/json" -X POST -d "{\"text\":\"我喜欢你\"}" http://172.18.1.146:9218/xinhuawang/senti/clf
curl -i -H "Content-Type: application/json" -X POST -d "{\"text\":\"我喜欢你\"}" http://172.18.1.146:9218/xinhuawang/senti/get_opinion_sentence
'''


@senti.route('/xinhuawang/senti/clf', methods=['GET', 'POST'])
def get_senti():
    print 'get in'
    func = 'get_sent'
    if request.method == 'POST':
        if not request.json or not 'text' in request.json:
            print 'xxxxxxxxxxxxxxxxxxxxx'
            return 'eror'
        text = request.json['text'].encode('utf-8')
    else:
        text = request.args.get('text').encode('utf-8')
    print text, type(text)
    # abort(400)
    try:
        score = model.clf3(text)
        rval = jsonify(score)
        logging.info("func: %s \t result: %s ", func, str(score))
    except Exception, e:
        traceback.print_exc()
        rval = 0.5
        rval = jsonify(rval)
        logging.error("func: %s \t error:%s!", func, str(e))
    return rval, 201


@senti.route('/xinhuawang/senti/get_opinion_sentence', methods=['GET', 'POST'])
def get_opinion_sentence():
    print 'get in'
    func = 'get_opinion_sents'
    if request.method == 'POST':
        if not request.json or not 'text' in request.json:
            print 'xxxxxxxxxxxxxxxxxxxxx'
            return 'eror'
        text = request.json['text'].encode('utf-8')
    else:
        text = request.args.get('text').encode('utf-8')
    try:
        rval = jsonify(model.get_opinion_sentence(text))
        logging.info("func: %s \t result: %s ", func, rval)
    except Exception, e:
        print e
        rval = []
        rval = jsonify(rval)
        logging.error("func: %s \t error:%s!", func, e)
    return rval, 201


if __name__ == '__main__':
    print 'start'
    senti.run(host='172.18.1.146', port=9218, debug=True)
    print 'end'
