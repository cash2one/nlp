# -*- coding: utf-8 -*-

import collections
import copy
import math
import os
import re
import sys

import Levenshtein
import gensim.models.phrases

import readfile as rf
import settings
import zaber_nlp as jieba
import zaber_nlp.posseg as pseg

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append("../preProcess")
sys.path.append("../similar/similar")

from preProcess import PreProcess

import time


class Keywords(object):
    def __init__(self, df_file, stopfile):
        """
        Brief:
            constructor of Keywords.
        """
        # self.synonym_model = Model("./synonym_dicts/synonym.txt", "./synonym_dicts/tyccl.txt",
        #                            "./synonym_dicts/redirect.txt", "./synonym_dicts/wiki_similar.txt",
        #                            "./synonym_dicts/vec.txt", only_synonym=True)
        self.update_period = 0  # minute
        self.updated_time = 0
        self.user_dicts = set()
        self.ner_dicts = set()
        self.prep = PreProcess()
        self.wd_df = rf.load_wd_df(df_file)
        self.stop_file = stopfile
        self.st_stopwords = rf.read_stopwords(stopfile)
        self.http = re.compile(r'(?:(?:https?:)|(?:www)|(?:wap))[\w\.\&\/\=\:\?%\-]+')
        self.nickname = re.compile(r'(?://@|@).{2,12}(?::| |,|，|\.)')
        self.pos_list = \
            {'vn': 1.0, \
             'vl': 1.0, \
             'l': 1.0, \
             'an': 1.0, \
             'n': 1.0, \
             'nl': 1.2, \
             'nr': 1.5, \
             'nrj': 1.5, \
             'nrt': 1.5, \
             'nrf': 1.5, \
             'nrfg': 1.5, \
             'ns': 1.3, \
             'nsf': 1.3, \
             'nt': 1.5, \
             'nz': 1.3, \
             'ng': 1.0, \
             'a': 0.5, \
             'al': 0.5, \
             'v': 1.0, \
             'shuming': 1.5}

    def update(self):
        now_time = time.time()
        if now_time - self.updated_time > self.update_period * 60:
            # 新词
            now_dict = rf.load_user_dict(settings.user_file)
            for w in self.user_dicts - now_dict:
                jieba.del_word(w[0])
            for word, freq, tag in now_dict - self.user_dicts:
                jieba.add_word(word, freq, tag)
            self.user_dicts = now_dict
            # 实体名称
            now_dict = self.merge_ner_dict()
            for w in self.ner_dicts - now_dict:
                jieba.del_word(w)
            for w in now_dict - self.ner_dicts:
                jieba.add_word(w, 100, 'nt')
            self.ner_dicts = now_dict
            # 停用词和噪声词
            self.st_stopwords = self.merge_stop_nosie()
            self.updated_time = now_time

    def merge_stop_nosie(self):
        stop_dict = rf.read_stopwords(self.stop_file)
        nosie_dict = rf.read_stopwords(settings.noise_file)
        merge_list = stop_dict | nosie_dict
        return merge_list

    def merge_ner_dict(self):
        stock_name, full_name = rf.read_public_company()
        stock_name = set(stock_name)
        full_name = set(full_name)
        merge_list = stock_name | full_name
        # merge_list = user_dict
        return merge_list

    def merge_ner_weight(self, key_dict):
        stock_name, full_name = rf.read_public_company()
        stock_dict = {}
        for i in range(len(stock_name)):
            stock_dict[full_name[i]] = stock_name[i]
        for key in key_dict.keys():
            if key in stock_dict.keys():
                if stock_dict[key] in key_dict.keys():
                    key_dict[stock_dict[key]][0] += key_dict[key][0]
                else:
                    key_dict[stock_dict[key]] = [0, 'nt']
                    key_dict[stock_dict[key]][0] = key_dict[key][0]
                del key_dict[key]
        return key_dict

    def filter_url(self, line):
        """
        Brief:
            used to filter all the urls.
        """
        l_http = self.http.findall(line)
        l_nickname = self.nickname.findall(line)
        res = line
        for url in l_http:
            res = res.replace(url, ' ')
        for nickname in l_nickname:
            res = res.replace(nickname, ' ')
        res = res.replace("com", "").replace("cn", "")
        return res

    def word_posseg(self, line):
        """
        Brief:
            jieba segmentation with both word and part of speech returned. 
        """
        l_words = [(obj.word.strip(), obj.flag) for obj in pseg.cut(line.strip()) if obj.word.strip()]
        # for tu in l_words:
        #     for i in tu:
        #         print i
        l_res = []
        flag = None
        flag_n_combine = False
        for pair in l_words:
            if pair[0] == u"·" and len(l_res) and 'nr' in l_res[-1][1]:
                l_res[-1] = (l_res[-1][0] + pair[0], l_res[-1][1])
                flag_n_combine = True
                flag = l_res[-1][1]
            elif flag and flag_n_combine and (
                                            'nr' in pair[1] or 'ns' in pair[1] or 'nt' in pair[1] or 'nz' in pair[
                                1] or 'n' ==
                            pair[1] or 'j' == pair[1]):
                flag = pair[1] if len(pair[1]) > len(l_res[-1][1]) else l_res[-1][1]
                l_res[-1] = (l_res[-1][0] + pair[0], flag)
            else:
                flag = None
                flag_n_combine = False
                if len(pair[0]) == 1: continue  # REMOVE single-character word
                l_res.append(pair)
        return l_res

    def bigram_keywords_extract_pos(self, ll_lines, min_count, threshold):
        """
        Brief:
            used to connect two words if their co-occurrence is high.
        Inputs:
            ll_lines(double list format): containing each line of the input text, which is represented as a list of (word,  part of speech) 2-tuples.
            min_count(int format): minimun number of co-occurence.
            threshold(int format): used to decide if it needs combine two words.
        Outputs:
            ll_bigram_lines(double list format): the same as the ll_lines, with some words modified.
        """
        ll_words = []
        ll_flags = []
        for l_line in ll_lines:
            ll_words.append([t[0] for t in l_line])
            ll_flags.append([t[1] for t in l_line])

        # 如果a、b 满足：(cnt(a, b) - min_count) * N / (cnt(a) * cnt(b)) > threshold, 就将其当成一个词，N是文本词的总数
        bigram = gensim.models.phrases.Phrases(ll_words, min_count=min_count, threshold=threshold, delimiter='_')
        ll_bigram_lines = []
        for i, l_line in enumerate(ll_words):
            l_tmp = bigram[l_line]
            l_flag = []
            if len(l_tmp) == len(l_line):
                ll_bigram_lines.append(ll_lines[i])
            else:
                k = 0
                for j, t in enumerate(l_tmp):
                    if l_line[k] != l_tmp[j]:
                        l_flag.append(ll_lines[i][k][1] + ' ' + ll_lines[i][k + 1][1])
                        k += 2
                    else:
                        l_flag.append(ll_lines[i][k][1])
                        k += 1
                ll_bigram_lines.append([(l_tmp[i], l_flag[i]) for i in range(len(l_tmp))])
        return ll_bigram_lines

    def get_weight_from_length(self, word):
        """
        Brief:
            based on word length, modify word weight.
        """
        lennum = 0
        L = len(word)
        if re.match(ur'\w+$', word):
            L *= 0.7
        if L <= 2:
            lennum = 0.5
        elif 2 < L <= 3:
            lennum = 1.2
        elif 3 < L <= 5:
            lennum = 1.4
        elif 5 < L <= 7:
            lennum = 1.7
        elif L > 7:
            lennum = 1.8
        return lennum

    def get_words_weight(self, ll_trigram_lines):
        """
        Brief:
            based on word frequency, modify  word weight.
        Inputs:
            ll_trigram_lines(double list format): containing each line of the input text, which is represented as a list of words.
        Outputs:
            d_words_weight(dict format): a dict whose keys are words,  whose values are (word weight, part of speech) 2-tuples.
        """
        d_words_weight = {}
        for l_trigram_line in ll_trigram_lines:
            for term in l_trigram_line:
                if term[0] in d_words_weight:
                    d_words_weight[term[0]][0] += 1
                else:
                    d_words_weight[term[0]] = [1, term[1]]

        for k in d_words_weight:
            d_words_weight[k][0] *= self.get_weight_from_length(k)
        return d_words_weight

    def filter_stopwords(self, d_words, delimiter='_'):
        """
        Brief:
            filter words for the trigram dictionary, based on the stopwords.
        """
        d_res = {}
        for word in d_words:
            flag = 0
            for term in word.split(delimiter):
                if term in self.st_stopwords:
                    flag = 1
                    break
            if flag != 1:
                d_res[word] = copy.deepcopy(d_words[word])
        # 将未录入的合成词重新写进词典里
        for word in d_words:
            if u'_' in word and word != u'_' and word not in d_res:
                label = d_words[word][1].split()
                words = word.split(u'_')
                try:
                    for i in range(len(words)):
                        item = words[i]
                        if label[i] in self.pos_list and item not in self.st_stopwords:
                            if item not in d_res:
                                d_res[item] = [d_words[word][0] * self.get_weight_from_length(item), label[i]]
                            else:
                                d_res[item][0] += d_words[word][0] * self.get_weight_from_length(item)
                except:
                    continue
        return d_res

    # def extract_stock(self, d_words):


    def filter_word_by_pos(self, d_words):
        """
        Brief:
            filter words based on the part of speech.
        """
        d_res = {}

        try:
            s_start_pos = {'n', 'v'}
            s_ner_pos = {'nt', 'nr', 'nz', 'ns'}
            s_end_pos = {'a', 'd', 'al', 'v', 'vn'}

            for word in d_words:
                # 单个的词语直接写进d_res中
                if u"_" not in word and d_words[word][1] in self.pos_list:
                    if word not in d_res:
                        d_res[word] = copy.deepcopy(d_words[word])
                        d_res[word][0] *= self.pos_list[d_words[word][1]]
                    else:
                        d_res[word][0] += d_words[word][0] * self.pos_list[d_words[word][1]]
                    continue
                multi_label = d_words[word][1]
                label = d_words[word][1].split()
                # 含有ner的bigram，只取出其中的ner部分。
                if len(label) >= 2 and (
                                        'nt' in multi_label or 'nr' in multi_label or 'nz' in multi_label or 'ns' in multi_label):
                    for idx in range(len(word.split('_'))):
                        l_w = word.split('_')
                        if label[idx] in self.pos_list:
                            if l_w[idx] in d_res:
                                d_res[l_w[idx]][0] += d_words[word][0] * self.pos_list[label[idx]]
                            else:
                                d_res[l_w[idx]] = [d_words[word][0] * self.pos_list[label[idx]], label[idx]]
                    # 保留这个合成词，权重给的极低，这样后面再录入为合成词时候不会重复计算这一部分的权重
                    d_res[word] = [0.01, multi_label]
                    continue
                # 主要留下名词性，不出现名词性+副词/形容词
                if len(label) >= 2 and label[0] in self.pos_list and \
                                label[-1] in self.pos_list and \
                                len(word) > 1 and \
                        not (label[0] in s_start_pos and label[-1] in s_end_pos):
                    d_res[word] = copy.deepcopy(d_words[word])
                    d_res[word][0] *= max(self.pos_list[label[0]], self.pos_list[label[-1]])
                # 动词名词组合
                if len(label) >= 2 and 'v' in label[0] and label[-1] == 'n':
                    d_res[word] = copy.deepcopy(d_words[word])
                    d_res[word][0] *= 2.0
                # 数字+英文
                if len(label) >= 2 and label[0] == 'm' and label[1] == 'eng' and 'v' not in label:
                    d_res[word] = copy.deepcopy(d_words[word])
                # 数字+中文
                if len(label) >= 2 and label[0] == 'm' and 'n' in label[1] and 'v' not in label:
                    d_res[word] = copy.deepcopy(d_words[word])
                # 单独的，词频大于等于4的，词长大于等于2的，动词
                if len(label) == 1 and label[0] == 'v' and len(word) >= 2 and d_words[word][0] >= 4:
                    d_res[word] = copy.deepcopy(d_words[word])
                # 两个数词在一起的情况，如“2014年”，“1800元”等
                if len(label) >= 2 and label[0] == 'm' and label[1] == 'm':
                    d_res[word] = copy.deepcopy(d_words[word])
                    d_res[word][0] *= 0.75
            # 将未录入的合成词重新写进词典里
            for word in d_words:
                if u'_' in word and word != u'_' and word not in d_res:
                    label = d_words[word][1].split()
                    words = word.split(u'_')
                    try:
                        for i in range(len(words)):
                            item = words[i]
                            if label[i] in self.pos_list:
                                if item not in d_res:
                                    d_res[item] = [d_words[word][0] * self.pos_list[label[i]], label[i]]
                                else:
                                    d_res[item][0] += d_words[word][0] * self.pos_list[label[i]]
                    except:
                        continue
            return d_res
        except Exception, e:
            # print  traceback.print_exc()
            return d_words

    def compute_idf(self, wordic):
        """
        Brief:
            compute idf value for each word.
        """
        for word in wordic:
            df = self.wd_df.get(word.strip(), -1)
            if df < 0:
                words = word.split('_')
                min_df = min([self.wd_df.get(i.strip(), -1) for i in words])
                if min_df < 0:
                    df = 1
                else:
                    df = min_df
            idf = math.log(settings.xinhua_doc_num / df, 10)
            wordic[word][0] *= 0.5 * idf
        return wordic

    def remove_delimiter_pos(self, d_words):
        """
        Brief:
            1. remove special symbol "_" for trigram word.
            2. some tricks dealing with blankspaces between words.
        """
        d_res = {}
        for t in d_words:
            t_value = d_words[t][0]
            # 保护字母/数字词语之间的"_"符号，变成"+"，如"5_G_网络"——>"5+G_网络"，"CEO_Gates"——>"CEO+Gates"
            t = re.sub(r'(?P<name1>\w+)_(?P<name2>\w+)', ur'\g<name1>+\g<name2>', t)
            # 将数字与字母词语之间的"+"重新变成"_"，如"5+G_网络"——>"5_G_网络"，"CEO+Gates"——>"CEO+Gates"
            t = re.sub(r'(?P<name1>\d+)\+(?P<name2>\w+)', ur'\g<name1>_\g<name2>', t)
            t = t.replace('+', ' ')
            t = t.replace('_', '')
            # 最后结果：5G网络，CEO Gates
            d_res[t] = t_value
        return d_res

    def remove_redundancy(self, d_words, thres):
        """
        Brief:
            based on the Levenshtein jaro function, remove some suspicious synonyms.
        """
        d_res = {}
        for word in d_words:
            flag = 0
            for another_word in d_words:
                # jaro formula: 1/3 *( m/s1 + m/s2 + 1 ), m is the length of common part.
                if word != another_word and Levenshtein.jaro(word, another_word) > thres and \
                                                2.0 / 3 < d_words[word] / (d_words[another_word] + 1) < 3.0 / 2:
                    if len(word) > len(another_word):
                        if word in d_res:
                            d_res[word] += d_words[another_word]
                        else:
                            d_res[word] = d_words[word] + d_words[another_word]
                    # 删除的条件：1.两者jaro相似度大于阈值（即其互为相近词的概率很大）
                    #            2.两者权重相差不大
                    #            3.删除词的长度都小于对比词
                    #            4.删除词、对比词权重比值在一定范围之内
                    elif d_words[word] < d_words[another_word]:
                        flag = 1
                        # break
                elif d_res.get(word, -1) < 0:
                    d_res[word] = d_words[word]
            if flag and word in d_res:
                del d_res[word]
        return d_res

    def get_topN_Phrase(self, d_words, topN):
        """
        Brief:
            use ordered dictionary to get top-n words.
        """
        d_ordered_res = collections.OrderedDict()
        for tup in sorted([(item[0], item[1]) for item in d_words.iteritems()], key=lambda x: x[1], reverse=True)[
                   :topN]:
            d_ordered_res[tup[0]] = tup[1]
        d_ordered_res = self.semantic_dup_remove(d_ordered_res)
        return d_ordered_res  # 如果返回json串， json.loads() 之后是无序的。

    def semantic_dup_remove(self, d_words):
        d_res = copy.deepcopy(d_words)
        words = set(d_words.keys())
        deleted_words = set()
        for k in d_words:
            if k not in deleted_words:
                words.remove(k)
                # l_tmp = self.synonym_model.synonym(k.encode("utf-8"))
                l_tmp = []
                for item1 in l_tmp:
                    for item2 in words:
                        if item1 == item2.encode("utf-8"):
                            deleted_words.add(item2)
                            try:
                                del d_res[item2]
                            except:
                                pass
        return d_res

    def normalize_weight(self, d_words):
        """
        Brief:
            use sqrt to reduce the interval of the word weights.
        """
        d_res = collections.OrderedDict()
        for key in d_words:
            try:
                d_res[key.encode("utf-8")] = round(math.sqrt(d_words[key]), 3)
            except:
                continue
        return d_res

    def pos_for_title(self, d_titles):
        d_res = {}
        for word in d_titles:
            if d_titles[word][1] in self.pos_list:
                d_res[word] = copy.deepcopy(d_titles[word])
                d_res[word][0] *= self.pos_list[d_titles[word][1]]
            if d_titles[word][1] == 'v n':
                d_res[word] = copy.deepcopy(d_titles[word])
                d_res[word][0] *= 1.5
        return d_res

    def handle_title(self, title):
        """
        Brief:
            add to satisfy the need of xinhuashe_multitags' need.
        Inputs:
        Outputs:
            l_res_titles: the list whose element of format (word, weight).
        """
        l_temp = self.word_posseg(title)
        l_tmp = []
        for item in l_temp:
            if len(l_tmp) and l_tmp[-1][1] == 'v' and item[1] == 'n':
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'v n')
            else:
                l_tmp.append(item)
        l_tmp = [l_tmp]
        d_res_titles = self.get_words_weight(l_tmp)
        d_res_titles = self.filter_stopwords(d_res_titles)
        d_res_titles = self.pos_for_title(d_res_titles)
        d_res_titles = self.compute_idf(d_res_titles)
        for word in d_res_titles:
            d_res_titles[word][0] *= self.title_times
        return d_res_titles

    def core_process(self, title, content):
        """
        Brief:
            main subroutine, will call bigram_keywords_extract_pos to get double word list, will call get_words_weight, filter_stopwords, filter_word_by_pos and compute_idf to get the word weight dictionary.
        Inputs:
        Outputs:
            d_words_filter_pos(dict format): a dict whose keys are words,  whose values are (word weight, part of speech) 2-tuples.
        """
        # 先对标题做单独处理
        d_res_titles = self.handle_title(title)
        ll_d = []
        # 提取一般的词语内容
        filter_text = self.filter_url(content)
        l_sents = re.split(ur',|"|”|“|、|\(|\)|（|）|《|》|，|。|：|！|；|_|\n| ', filter_text)
        for sent in l_sents:
            if sent.strip():
                ll_d.append(self.word_posseg(sent))
        ll_bigram_lines = self.bigram_keywords_extract_pos(ll_d, settings.bigram_min_count, settings.bigram_threshold)
        d_words_weight = self.get_words_weight(ll_bigram_lines)
        d_words_filter_stop = self.filter_stopwords(d_words_weight)
        d_words_filter_pos = self.filter_word_by_pos(d_words_filter_stop)
        d_words_filter_pos = self.compute_idf(d_words_filter_pos)
        # 合并title的结果和content的结果
        for key in d_res_titles:
            if key not in d_words_filter_pos:
                d_words_filter_pos[key] = copy.deepcopy(d_res_titles[key])
            else:
                d_words_filter_pos[key][0] += d_res_titles[key][0]
        # 合并公司以及股票的权重
        d_words_filter_pos = self.merge_ner_weight(d_words_filter_pos)
        return d_words_filter_pos

    def process(self, content, topN, title=''):
        """
        Brief:
            main function, will call core_process to get initial word dictionary, will call remove_delimiter_pos, remove_redundancy, get_topN_Phrase and normalize_weight to get the final word weight dictionary.
        Inputs:
        Outputs:
            an ordered dictionary whose keys are the words, whose values are the weights.
        """
        self.update()
        self.title_times = min(4.0, len(content) / (len(title) + 1) / 35)
        title = self.prep.normalize(title).decode("utf-8")
        content = self.prep.normalize(content).decode("utf-8")
        d_words_texts = self.core_process(title, content)
        d_words_repl = self.remove_delimiter_pos(d_words_texts)
        d_words_rm_redunt = self.remove_redundancy(d_words_repl, settings.similarity_threshold)
        d_words_topN = self.get_topN_Phrase(d_words_rm_redunt, topN)
        return self.normalize_weight(d_words_topN)


if __name__ == '__main__':
    text = '''
    Apple Co.ltd道德卫士我们可以002430蓝黛传动0024301看到重庆蓝黛动力传动机械股份有限公司这种绘图方式实际上傅顶啥是按命令傅顶啥添加的'''

    topN = 1000
    kw = Keywords(settings.df_file, settings.stopwords)
    d_res = kw.process(text, topN, '')
    for k, v in d_res.items()[0:50]:
        print k, v
    time.sleep(10)
    kw.update()
    d_res = kw.process(text, topN, '')
    for k, v in d_res.items()[0:50]:
        print k, v
