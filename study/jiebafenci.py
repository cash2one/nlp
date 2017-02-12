# -*- coding: utf-8 -*-
import time

import jieba.posseg as pseg

# reload(sys)                      # reload 才能调用 setdefaultencoding 方法
# sys.setdefaultencoding('utf-8')  # 设置 'utf-8'
t1 = time.time()
f = open("origin/news_orig.txt", "r")  # 读取文本
string = f.read().decode("utf-8")
string = "沒有我們第三代你們妳們他們她們是否 "
words = pseg.cut(string)  # 进行分词
result = ""  # 记录最终结果的变量
for w in words:
    word = str(w.word.encode('utf-8'))
    flag = str(w.flag)
    result += word + "/" + str(w.flag)  # 加词性标注

# f = open("t_with_POS_tag.txt", "w")  # 将结果保存到另一个文档中
# f.write(result)
# f.close()
print result
t2 = time.time()
print("分词及词性标注完成，耗时：" + str(t2 - t1) + "秒。")  # 反馈结果
