#encoding=utf-8
from __future__ import print_function, unicode_literals
import sys
sys.path.append("../")
import zaberFenci
zaberFenci.load_userdict("userdict.txt")
import zaberFenci.posseg as pseg

zaberFenci.add_word('石墨烯')
zaberFenci.add_word('凱特琳')
zaberFenci.del_word('自定义词')

test_sent = (
"李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
"例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
"「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
)
words = zaberFenci.cut(test_sent)
print('/'.join(words))

print("="*40)

result = pseg.cut(test_sent)

for w in result:
    print(w.word, "/", w.flag, ", ", end=' ')

print("\n" + "="*40)

terms = zaberFenci.cut('easy_install is great')
print('/'.join(terms))
terms = zaberFenci.cut('python 的正则表达式是好用的')
print('/'.join(terms))

print("="*40)
# test frequency tune
testlist = [
('今天天气不错', ('今天', '天气')),
('如果放到post中将出错。', ('中', '将')),
('我们中出了一个叛徒', ('中', '出')),
]

for sent, seg in testlist:
    print('/'.join(zaberFenci.cut(sent, HMM=False)))
    word = ''.join(seg)
    print('%s Before: %s, After: %s' % (word, zaberFenci.get_FREQ(word), zaberFenci.suggest_freq(seg, True)))
    print('/'.join(zaberFenci.cut(sent, HMM=False)))
    print("-"*40)
