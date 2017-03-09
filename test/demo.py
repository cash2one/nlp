# encoding=utf-8
from __future__ import unicode_literals

import zaber_nlp.analyse

print('=' * 40)
print('1. 分词')
print('-' * 40)

seg_list = zaber_nlp.cut("2012厦门国际聆听者将于1月7日举行厦门国际马拉松赛")
print(" " + "/ ".join(seg_list))  # 默认模式

seg_list = zaber_nlp.cut("羽球女单李雪芮率先亮相 横扫对手获小组开门红_网易体育")
print(" " + "/ ".join(seg_list))

print('=' * 40)
print(u'2. 添加新词典/调整词典')
print('-' * 40)

print('/'.join(zaber_nlp.cut('如果放到post中将出错。')))
# 如果/放到/post/中将/出错/。
print(zaber_nlp.suggest_freq(('中', '将'), True))
# 494
print('/'.join(zaber_nlp.cut('如果放到post中将出错。')))
# 如果/放到/post/中/将/出错/。
print('/'.join(zaber_nlp.cut('「台中」正确应该不会被切开')))
# 「/台/中/」/正确/应该/不会/被/切开
print(zaber_nlp.suggest_freq('台中', True))
# 69
print('/'.join(zaber_nlp.cut('「台中」正确应该不会被切开')))
# 「/台中/」/正确/应该/不会/被/切开

print('=' * 40)
print('关键词提取')
print('-' * 40)

s = "此外，露宿者拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，" \
    "增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置" \
    "业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市" \
    "商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"

print(' TextRank')
print('-' * 40)

for x, w in zaber_nlp.analyse.Text_Rank(s, allowPOS='n', withWeight=True, withFlag=True):
    print('%s %s' % (x, w))

print('=' * 40)
print('3. 词性标注')
print('-' * 40)

words = zaber_nlp.posseg.cut("2012厦门国际马拉松将于1月7日举行厦门国际马拉松赛")
for word, flag in words:
    print('%s %s' % (word, flag))

print('=' * 40)

content = open("../study/origin/aa", "rb").read()
# zaber_nlp.cut(content)
# print("Default Mode: " + "/ ".join(zaber_nlp.cut(content)))  # 默认模式
zaber_nlp.analyse.set_stop_words("./stop_words.txt")
for x, w in zaber_nlp.analyse.Text_Rank(content, withWeight=True, topK=10):
    print('%s %s' % (x, w))

content = open("../study/origin/aa", "rb").read()
zaber_nlp.analyse.Associate(content)
zaber_nlp.analyse.Associate_find(content)
