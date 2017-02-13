# encoding=utf-8
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('gbk')
sys.path.append("../")

import zaber_nlp.analyse

print('=' * 40)
print('1. 分词')
print('-' * 40)

seg_list = zaber_nlp.cut(u"我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = zaber_nlp.cut(u"我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 默认模式

seg_list = zaber_nlp.cut(u"他来到了网易杭研大厦")
print(", ".join(seg_list))

print('=' * 40)
print(u'2. 添加自定义词典/调整词典')
print('-' * 40)

print('/'.join(zaber_nlp.cut('如果放到post中将出错。', HMM=False)))
# 如果/放到/post/中将/出错/。
print(zaber_nlp.suggest_freq(('中', '将'), True))
# 494
print('/'.join(zaber_nlp.cut('如果放到post中将出错。', HMM=False)))
# 如果/放到/post/中/将/出错/。
print('/'.join(zaber_nlp.cut('「台中」正确应该不会被切开', HMM=False)))
# 「/台/中/」/正确/应该/不会/被/切开
print(zaber_nlp.suggest_freq('台中', True))
# 69
print('/'.join(zaber_nlp.cut('「台中」正确应该不会被切开', HMM=False)))
# 「/台中/」/正确/应该/不会/被/切开

print('=' * 40)
print('3. 关键词提取')
print('-' * 40)
# print(' TF-IDF')
# print('-' * 40)

s = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，" \
    "增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置" \
    "业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市" \
    "商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"
# for x, w in zaber_nlp.analyse.extract_tags(s, withWeight=True):
#     print('%s %s' % (x, w))
#
# print('-' * 40)
print(' TextRank')
print('-' * 40)

for x, w in zaber_nlp.analyse.textrank(s, withWeight=True):
    print('%s %s' % (x, w))

print('=' * 40)
print('4. 词性标注')
print('-' * 40)

words = zaber_nlp.posseg.cut("我爱北京天安门")
for word, flag in words:
    print('%s %s' % (word, flag))

print('=' * 40)
print('6. Tokenize: 返回词语在原文的起止位置')
print('-' * 40)
print(' 默认模式')
print('-' * 40)

result = zaber_nlp.tokenize('永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0], tk[1], tk[2]))

print('-' * 40)


