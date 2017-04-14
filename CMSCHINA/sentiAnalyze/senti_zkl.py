# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import pickle
import tensorflow as tf
import numpy as np
from corpus_handel import load_data_and_labels
import json
import pickle
import os
import time
import ahocorasick

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append("../preProcess")

from preProcess import PreProcess

# def test(
end_fuhao = ['.', '。', '!', '?', '！', '？']
no_end_fuhao = [',', '，', ';', '；', '-', ':', '：', '“', '”', '"']
fuhao = end_fuhao + no_end_fuhao


class Classify():
    def __init__(self):
        self.A, self.senti_dicts = self.build_A('senti_dict.txt')
        _dir = cur_dir + '/../autoSummary/'
        self.O, self.opinion_dicts = self.build_O('opinion_dicts.txt')
        # self.tr4s = TextRank4Sentence(
        #    stop_words_file = _dir+'./stopword.data', noise_words_file = _dir+'./noisewords.txt', 
        #    use_speech_flag_filter = True, use_stop_words = True)
        # self.summary = self.tr4s.get_sent_weight
        model_dir = './result/ai_online/'
        checkpoint_file = model_dir + 'checkpoints/model-90635'
        # model_dir = './xinhuashe_model/'
        # checkpoint_file = model_dir + 'checkpoints/model-99033'
        '''
        model_dir = './result/small/'
        checkpoint_file = model_dir + 'checkpoints/model-400'
        '''
        vocabulary_path = os.path.join(model_dir, 'vocabulary_dict')
        self.vocabulary = pickle.load(open(vocabulary_path, 'r'))
        graph = tf.Graph()
        self.sequence_length = 100
        self.predictions = None
        self.input_x = None
        self.dropout_keep_prob = None
        self.sess = None
        self.prep = PreProcess()

        with graph.as_default():
            session_conf = tf.ConfigProto(
                device_count={'GPU': 0},
                allow_soft_placement=True,
                log_device_placement=False, )
            # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333))
            self.sess = tf.InteractiveSession(config=session_conf)
            with self.sess.as_default():
                saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
                saver.restore(self.sess, checkpoint_file)

                self.input_x = graph.get_operation_by_name("input_x").outputs[0]
                self.dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
                self.predictions = graph.get_operation_by_name("output/prob").outputs[0]
                #             pickle.dump(self.predictions,open('v1.pkl','w'))

    def read_opinion_dicts(self, path):
        rval = []
        ii = open(path, 'r')
        for line in ii:
            rval.append(line.strip())
        return rval

    def test_data_word_embedding(self, test_text_list):
        final_sentence_list = []
        test_text_list = [test_text.strip() for test_text in test_text_list]
        try:
            test_text_list = [list(test_text.decode('utf-8')) for test_text in test_text_list]
        except:
            test_text_list = [list(test_text) for test_text in test_text_list]
        for test_text in test_text_list:
            num_padding = self.sequence_length - len(test_text)
            new_sentence = []
            if num_padding < 0:
                new_sentence = test_text[:self.sequence_length]
            else:
                new_sentence = test_text + ["<PAD/>"] * num_padding
            temp_sentence = []
            for word in new_sentence:
                try:
                    word = word.encode('utf-8')
                except:
                    word = word
                if self.vocabulary.has_key(word):
                    temp_sentence.append(word)
                else:
                    temp_sentence.append('<PAD/>')
            final_sentence_list.append([self.vocabulary[word] for word in temp_sentence])
        x_test = np.array(final_sentence_list)
        return x_test

    def build_O(self, path):
        A = ahocorasick.Automaton()
        rval = {}
        for line in open(path, 'r'):
            w = line.strip()
            A.add_word(w, w)
        A.make_automaton()
        return A, rval

    def build_A(self, path):
        A = ahocorasick.Automaton()
        rval = {}
        for line in open(path, 'r'):
            w, f = line.strip().split('\t')
            if f == '1' or f == '-1':
                A.add_word(w, w)
        A.make_automaton()
        return A, rval
        '''
        if list(A.keys())==[]:return []
        locations=[[key,end_idx-len(key)+1,end_idx+1] for end_idx, key in A.iter(text)]
        '''

    def clf3(self, sentence):
        if not list(self.A.iter(sentence)):
            return 0.5
        else:
            return self.clf(sentence)

    def clf(self, sentence):
        print sentence
        sentence = self.prep.normalize(sentence)
        x_test = self.test_data_word_embedding([sentence])
        prob = self.predictions.eval(session=self.sess, feed_dict={self.input_x: x_test, self.dropout_keep_prob: 0.5})
        return float("%.2f" % prob[0, 0])

    def get_opinion_sentence(self, text):
        # print text
        '''
        规则:
        从规则词后面开始，若后面直接是标点符号则不结束
        遇到其他opinion词则在上一个标点符号结束
        遇到句号则结束
        规则词后面恰好是"，直接跳到下一个"继续
        若规则词后面是句号，则往前找...
        '''
        rval = []
        data = self.O.iter(text)
        locations = [[key, end_idx - len(key) + 1, end_idx + 1] for end_idx, key in data]
        for k, (key, bgin, end) in enumerate(locations):
            pre_sent = u''
            text2 = text[:end].decode('utf-8')
            for j in range(len(text2) - 1, -1, -1):
                if text2[j] in fuhao or j == 0:
                    pre_sent = text2[j + 1:]
                    break
            if k != len(locations) - 1:
                sent = text[end:locations[k + 1][1]].decode('utf-8')
                ###下一个词前一个符号截断
                for j in range(len(sent) - 1, -1, -1):
                    if sent[j] in fuhao:
                        sent = sent[:j + 1]
                        break
            else:
                sent = text[end:].decode('utf-8')
            k = 0
            print 'sent=', sent
            while k < len(sent):
                if k == 0:
                    if sent[k].encode('utf-8') in end_fuhao:
                        break
                    bgn = sent.find('“'.decode('utf-8'))
                    if bgn != -1 and bgn <= 2:
                        net = sent.find('”'.decode('utf-8'))
                        rval.append((key, pre_sent + sent[bgn + 1:net]))
                        break
                    if sent[k].encode('utf-8') in no_end_fuhao:
                        while sent[k].encode('utf-8') in no_end_fuhao and k < len(sent):
                            k = k + 1
                elif sent[k] in end_fuhao or k + 1 == len(sent):
                    print 'xxxxxxxxxxxxxxxxx', sent[k]
                    rval.append((key, pre_sent + sent[:k]))
                    break
                k += 1
        return [(key, sent.encode('utf-8')) for key, sent in rval]

    '''
    def get_opinion_sentence(self, text, topn=10, topratio=0.1, ratio=0.5):
        summary=self.summary(text)
        summary2=[]
        def cut_sents(x):
            return [x]
        for sent,value in summary:
            sents=cut_sents(sent)
            for s in sents:
                summary2.append((s,value))#TODO:value应该变吗
        summary=summary2

        sents=[str(x[0]) for x in summary]
        for sent in sents:print sent
        key_weights=[x[1] for x in summary]
        print key_weights 
        sentis=[self.clf3(sent) for sent in sents]
        senti_weights=[abs(x-0.5) for x in sentis]
        weights=zip(key_weights, senti_weights)
        data=[(sents[i],weights[i],i) for i in range(len(sents))]
        
        filter_func=lambda x: x[1][1]>0.25
        data=filter(filter_func, data)
        sort_func=lambda x: x[1][0]+ratio*x[1][1]
        data=sorted(data, key=sort_func, reverse=True)
        #TODO 需要根据不同的情况重新计算topn
        return [(data[i][0],sentis[data[i][2]],key_weights[data[i][2]]) for i in range(topn)]
    '''


if __name__ == "__main__":
    classify = Classify()
    sents = ['我心情很好', '京东', '淘宝', '蚂蚁', '水沟', '贵州高等教育毛入学率达31.1%', \
             '不知道今天在幼儿园乖乖吃饭，睡觉了没有#秋色#', \
             'Facebook、谷歌、微软 为什么大家都在投资人工智能？', \
             '会玩的人生才是靠谱', \
             '黑金会员，全场9.2折！就在9月28日', \
             '银谷财富忽悠术！ 虚伪，虚假，都看看吧！@点融网 @红岭创投', \
             '看手机贷怎么靠大数据速审，在贷款平台杀出一条血路', \
             '打破春节月光魔咒 手机贷缓解用钱压力', \
             '有利网上线半年交易额破亿元', \
             '大数据解析乌兹别克：两项居12强之首 严防国安铁卫',
             '大宝小贝',
             '银汉游戏旗下《时空召唤》携游戏女神Angelababy一起开黑', \
             '连连支付 连缀贫困儿童希望之路',
             '不辜负人民的期望',
             '华为收入曝光！任正非：不上市则有可能称霸世界！',
             '#华为nova#快乐是我的不2法则#买手机得上苏宁易购#',
             '就像让东风标致、东风雪铁龙以小米加步枪的装备，顶着飞机加大炮的狂轰滥炸往前冲，这无异于以卵击石。', \
             '杭州装上“城市数据大脑” 首战交通拥堵 阿里云人工智能ET当起交通警察']
    # sents=['你真美']
    for sent in sents:
        # print sent,classify.clf(sent)
        print sent, classify.clf(sent)
        print sent, classify.clf(sent)
        print sent, classify.clf(sent)
        # print sent,classify.clf(sent),classify.clf3(sent)

    text = '''
        俄罗斯总统弗拉基米尔·普京为中国在中亚地区杰出的经济主导地位感到困扰，或许会欢迎来自日本之类的国家的投资。          无论怎样，未来几个月，我们将会看到旨在促进日俄关系的热烈外交举措。安倍将于下个月出访符拉迪沃斯托克，而普京也计划
            于今年年底之前访问日本。      在公众场合，安倍则不得不收敛他对于俄罗斯的热情，希望不要因此惹怒美国和欧洲。      但是>    ，想要和俄罗斯合作的期盼之情在日本官员之间还是显而易见的。（曾庆睿译　洪漫校
        '''
    print json.dumps(classify.get_opinion_sentence(text), ensure_ascii=False)
