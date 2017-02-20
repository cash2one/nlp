# encoding=utf-8
from __future__ import print_function, unicode_literals

import sys

sys.path.append("../")
import zaber_nlp
import zaber_nlp.posseg as pseg

zaber_nlp.add_word('周泽彪')
zaber_nlp.add_word('凱特琳')
zaber_nlp.del_word('自定义词')
print('=' * 40)
print(u'2. 添加新词典/调整词典')
print('-' * 40)
test_sent = (
    "北京百分点信息科技有限公司成立于2009年，是中国领先的大数据技术与应用服务商。"
)
words = zaber_nlp.cut(test_sent)
print('/'.join(words))
zaber_nlp.load_userdict("userdict.txt")
words = zaber_nlp.posseg.cut(test_sent)
for word, flag in words:
    print('%s %s' % (word, flag))

print("=" * 40)

result = pseg.cut(test_sent)

for w in result:
    print(w.word, "/", w.flag, ", ", end=' ')

print("\n" + "=" * 40)

terms = zaber_nlp.cut('easy_install is great')
print('/'.join(terms))
terms = zaber_nlp.cut('python 的正则表达式是好用的')
print('/'.join(terms))

print("=" * 40)
# test frequency tune
testlist = [
    ('今天天气不错', ('今天', '天气')),
    ('如果放到post中将出错。', ('中', '将')),
    ('我们中出了一个叛徒', ('中', '出')),
]

for sent, seg in testlist:
    print('/'.join(zaber_nlp.cut(sent)))
    word = ''.join(seg)
    print('%s Before: %s, After: %s' % (word, zaber_nlp.get_FREQ(word), zaber_nlp.suggest_freq(seg, True)))
    print('/'.join(zaber_nlp.cut(sent)))
    print("-" * 40)
