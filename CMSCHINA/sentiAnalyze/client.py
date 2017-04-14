# encoding=utf-8
import json
from gen.sentiment.SentimentService import Client
from bfd.harpc.common import config
from bfd.harpc import client
import sys, os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()


def usage():
    print "usage:"
    print "python client_sample.py"


if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/client.conf.' + branch
    conf = config.Config(conf_path)
    manager = client.Client(Client, conf)
    client_ = manager.create_proxy()
    print dir(client_)
    word = '你真美'
    res = client_.get_sentiment(word, 'clf')
    d_res = json.loads(res)
    print res

    res = client_.get_sentiment(word, 'clf3')
    d_res = json.loads(res)
    print res

    text = '''
    《西游伏妖篇》星爷:我最喜欢猪八戒亲吻蜘蛛精的情节

原标题：星爷:我最喜欢 猪八戒亲吻蜘蛛精的情节


《西游伏妖篇》佛山谢票

周星驰编剧、徐克导演的《西游伏妖篇》大年初一上映后,第九天就已经突破19亿票房,成为今年春节档的票房霸主。昨天,周星驰携林允来到广东佛山向观众谢票,并且为影片的后续发劲再添一把火。

从小喜爱武术的星爷来到武术之乡与当地影迷聊起了自己的习武经历,还表示:“我超级喜欢粤语长片《如来神掌》。”他还顺势提问影迷:“谁知道如来神掌第十式是什么?答对了还有利是。”有一位星爷忠实的影迷立刻答道:“如来灭魔。”星爷听后也竖起大拇指夸赞:“厉害。”

粤语“西游”更过瘾

当天,观众在观看粤语版《西游伏妖篇》过程中欢笑声不断,看到唐僧和孙悟空相爱相杀的师徒之情,观众纷纷表示:“粤语版里这对师傅更可爱,周氏喜剧更浓重。”不过也有观众提出:“故事里,唐僧怎么都向悟空下跪了?是不是太颠覆。”现场,星爷解释道:“唐僧带着三个妖怪徒弟取经,要懂得怎么管理他们。他是一个很有智慧的人,不同的情况要有不同的方法,他情商很高。”
'''
    res = client_.get_opinion_sentence(text, 0.5)
    # d_res = json.loads(res, ensure_ascii=False)
    print res
