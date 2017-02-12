# -*- coding: utf-8 -*-  
import os
import time

import jieba
import pylab

import NovelRecommend

# 由搜狗语料库 生成数据
folder_path = 'E:/PycharmProjects/nlp/SogouC.reduced/Reduced'
# 找到该文件夹下面的文件夹集合
folder_list = os.listdir(folder_path)
class_list = []
# 由于乱码等问题 仅以数字[0,1,...]来代表文件分类
nClass = 0
N = 100  # 每类文件 最多取 100 个样本 70%train 30%test
train_set = []
test_set = []
all_words = {}

process_times = []  # 统计处理每个文件的时间
for i in range(len(folder_list)):
    # 遍历文件夹
    new_folder_path = folder_path + '\\' + folder_list[i]
    files = os.listdir(new_folder_path)
    class_list.append(nClass)
    # 文件夹类别
    nClass += 1
    j = 0
    nFile = min([len(files), N])
    for f in files:
        if j > N:
            break
        start_time = time.clock()

        complete_path = open(new_folder_path + '\\' + f, 'r')
        raw = complete_path.read()
        word_cut = jieba.cut(raw, cut_all=False)  # 结巴分词
        word_list = list(word_cut)
        for word in word_list:
            if word in all_words.keys():
                all_words[word] += 1
            else:
                all_words[word] = 0
        if j > 0.3 * nFile:
            train_set.append((word_list, class_list[i]))
        else:
            test_set.append((word_list, class_list[i]))
        j += 1
        end_time = time.clock()
        process_times.append(end_time - start_time)

        print "Folder ", i, "-file-", j, "all_words length = ", len(all_words.keys()), \
            "process time:", (end_time - start_time)

print len(all_words)

# 根据word的词频排序
all_words_list = sorted(all_words.items(), key=lambda e: e[1], reverse=True)
word_features = []
# 由于乱码的问题，没有正确使用 stopwords；简单去掉 前100个高频项
# word_features 是选用的 word-词典
for t in range(100, 1100, 1):
    word_features.append(all_words_list[t][0])


def document_features(document):
    document_words = set(document)
    features = {}
    for w in word_features:  # 根据词典生成 每个document的feature True or False
        features['contains(%s)' % w] = (w in document_words)
    return features


# 根据每个document 分词生成的 word_list 生成 feature
train_data = [(document_features(d), c) for (d, c) in train_set]
test_data = [(document_features(d), c) for (d, c) in test_set]
print "train number:", len(train_data), "\n test number:", len(test_data)

# 朴素贝叶斯分类器
classifier = NovelRecommend.NaiveBayesClassifier.train(train_data)
print "test accuracy:", NovelRecommend.classify.accuracy(classifier, test_data)

# 处理每个文件所用的时间 可见到后面 处理单个文件的时间显著增长
# 原因 已查明


pylab.plot(range(len(process_times)), process_times, 'b.')
pylab.show()
