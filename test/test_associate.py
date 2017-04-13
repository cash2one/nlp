# encoding=utf-8

import os
import time

import zaber_nlp.analyse

# 由搜狗语料库 生成数据
folder_path = 'E:/PycharmProjects/nlp/study/SogouC.reduced/Reduced'
# 找到该文件夹下面的文件夹集合
folder_list = os.listdir(folder_path)
N = 1800
process_times = []  # 统计处理每个文件的时间
sum_all_files = 0
for i in range(len(folder_list)):
    # 遍历文件夹
    new_folder_path = folder_path + '\\' + folder_list[i]
    files = os.listdir(new_folder_path)
    j = 0
    sum_all_files += N
    start_time = time.clock()
    for f in files:
        if j > N:
            break
        complete_path = open(new_folder_path + '\\' + f, 'r')
        raw = complete_path.read()
        result1 = zaber_nlp.analyse.pyahocorasick(raw)
        j += 1
    end_time = time.clock()
    process_times.append(end_time - start_time)
    print "Folder ", i, "has files", N, \
        "process time:", (end_time - start_time)
print "it cost time:", sum(process_times), "the number of files:", sum_all_files


# zaber_nlp.analyse.Associate_find(content)
