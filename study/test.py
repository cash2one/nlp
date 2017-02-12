# coding:utf8
from __future__ import division
import numpy as np
import jieba
import re
import jieba.analyse
from collections import Counter,defaultdict

# file_name = 'dict/stopwords_tw.txt'
# jieba.analyse.set_stop_words(file_name)
# jieba.set_dictionary('dict/dict.txt.big')
def coocurance(text,windows=3):

    word_lst = [e for e in jieba.lcut(text) ]

    # print '/'.join(word_lst)
    data = defaultdict(Counter)
    for i,word in enumerate(word_lst):
        indexStart = i - windows
        indexEnd = i + windows
        if indexStart < 0:
            temp = Counter(word_lst[:windows+1+i])
            temp.pop(word)
            data[word] += temp
            # print word
        elif indexStart>=0 and indexEnd<=len(word_lst):
            temp = Counter(word_lst[i-windows:i+windows+1])
            temp.pop(word)
            data[word] += temp
            # print word
        else:
            temp = Counter(word_lst[i-windows:])
            temp.pop(word)
            data[word]+=temp
            # print word
    return data


def printDict(data):
    ''' print out dict of dict  '''
    for k,v in data.items():
        for k1,v1 in v.items():
            print k,k1,v1

def textRank(graph,d=0.85,kw_num=3,with_weight=False):
    TR = defaultdict(float,[(word,1.) for word,cooc in graph.items()]) # TextRank graph with default 1
    TR_prev = TR.copy()
    err = 1e-4
    error = 1
    iter_no = 100
    index = 1
    while (iter_no >index and  error > err):
        error = 0
        TR_prev = TR.copy()
        for word,cooc in graph.items():
            temp=0
            for link_word,weight in cooc.items():
                temp += d*TR[link_word]*weight/sum(graph[link_word].values())
                # print 'temp:',temp
            TR[word] = 1 -d + temp
            # print 'word:%s,TR:%.2f'%(word.encode('utf8'),TR[word])

            # print 'TR[{}]:{}'.format(word.encode('utf8'),TR[word])
            # print '----'
        error += (TR[word] - TR_prev[word])**2
        # print '-'*40
        # print 'keywords finding...iter_no:{},\terror:{}'.format(index,error)
        index += 1
    if with_weight:
        kw = sorted(TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)
        kw = [(k,v/max(zip(*kw)[1])) for k,v in kw ][:kw_num]
    else:
        kw = [word for word,weight in sorted(TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)[:kw_num]]
    return kw

def abstractTextRank(graph,d=0.85,sent_num=3,with_weight=False):
    sent_TR = defaultdict(float,[(sent,np.random.rand()) for sent,_ in graph.items()])

    err = 1e-5
    error = 1
    iter_no = 100
    index = 1
    while (iter_no >index and  error > err):
        error = 0
        sent_TR_prev = sent_TR.copy()
        for sent,cooc in graph.items():
            temp = 0
            for link_sent,weight in cooc.items():
                temp += d*sent_TR[link_sent]*weight/sum(graph[link_sent].values())
                # print 'add temp:',temp
            # print '----'
            sent_TR[sent] = 1 -d + temp
        error += (sent_TR[sent] - sent_TR_prev[sent])**2

        print 'key sentence finding...iter_no:{},\terror:{}'.format(index,error)
        index += 1
    if with_weight:
        ks = sorted(sent_TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)
        ks = [(k,v/max(zip(*ks)[1])) for k,v in ks ][:sent_num]
    else:
        ks = [sent for sent,weight in sorted(sent_TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)[:sent_num]]
    return ks



def sentence_coocurance(text,kw_num=3):
    ## sentence_kw :
    ## {'sen1':[word1,word2,word3],'sen2':[word2,word3,word4],
    ##  'sen3':[word1,word3,word5]}
    # sentence_kw = {'A':[1,2,3],'B':[2,3,4],'C':[1,3,5]} # test used!!
    docs = re.split(u'，|。',text)
    sentence_kw = defaultdict(list)
    for sen in docs:
        if sen == u'':
            continue
        keywords = textRank(coocurance(text,windows=5),kw_num=kw_num)
        sentence_kw[sen] = keywords

    cooc_dict = defaultdict(dict) # coocurance sentence with respect to keywords

    for sentence,kw in sentence_kw.items():
        # cooc_dict[sentence] = {sentence:0}
        temp = {}
        for sent_check, kw_check in sentence_kw.items():
            if sentence == sent_check:
                # print 'nope'
                temp[sentence] =0
                continue
            else:
                count = 0
                for word in kw:
                    if word in kw_check:
                        count+=1
                # print 'yes:\t',count
                temp[sent_check] = count
        cooc_dict[sentence] = temp
    return cooc_dict



if __name__ == '__main__':

    ## load stop words ##
    # with open(file_name) as f:
    #     doc = f.read()
    # doc = doc.decode('utf8')
    # doc = re.sub('\r\n','\n',doc)
    # global STOP_WORDS
    # STOP_WORDS = doc.split('\n')
    #

    text = u'賣鮮花的漂亮女孩在買鮮花'
    text1 = u'''
    新华社日内瓦1月18日电（记者刘畅郝薇薇）18日，国家主席习近平在日内瓦万国宫会见第71届联合国大会主席汤姆森和联合国秘书长古特雷斯，强调中国坚定走多边主义道路，捍卫联合国宪章宗旨和原则，支持联合国为维护世界和平、促进共同发展发挥更大作用。

　　习近平指出，联合国是最具普遍性、代表性、权威性的政府间国际组织，应该在全球治理中发挥核心作用。当前形势下，联合国的作用需要增强，而不是削弱。在各种全球性威胁和挑战面前，要坚定走多边主义道路。中国是第一个在联合国宪章上签字的国家，将继续坚定支持联合国事业，继续做联合国坚定的合作伙伴。

　　习近平强调，经济全球化是生产力发展的必然结果和客观需要，是历史前进的大势。要更好地适应、引导、管理经济全球化，让经济全球化的正面效应更多释放出来。全球治理是经济全球化的必然要求。各国利益与共，命运相连，必须摒弃逐利争霸的旧模式，走以制度、规则来协调关系和利益的新道路。中国一贯主张各国平等相待，走符合自身国情的发展道路，共同努力，互利共赢。我们走中国特色社会主义道路取得了一些治国理政经验，愿通过联合国这个平台同各国分享。中国提出“一带一路”倡议就是为了同各国分享发展机遇和成果。希望联合国在落实2030年可持续发展议程方面有更大作为。

　　汤姆森和古特雷斯表示，习近平主席昨天在世界经济论坛年会上重申中国政府致力于多边主义，受到国际社会高度评价。这对联合国和多边事业是重要保障。当今的全球性挑战，需要国际社会成员携手面对。长期以来，中国在应对气候变化、减贫、可持续发展、预防外交、维和等领域发挥了积极领导作用。联合国愿同中国共同推进世界和平与发展事业，实现构建人类命运共同体的伟大理想。

　　会见后，古特雷斯向习近平赠送周恩来总理1954年率团出席日内瓦会议的珍贵历史文件和1945年各国签署的《联合国宪章》正本复印件。
    '''
    text2 = u'''
    现在许多企业呼声最普遍的一个问题，就是各种‘费’不仅项目繁多，而且征收不规范。”总理说，“一个企业要对应许多个收费机构、部门，甚至还有中介等单位，经营人员根本不明就里。一些地方和部门收费标准还各不相同，自由裁量权过大。”

　　他强调，年底前要建立政府定价管理的涉企收费目录清单制度，给企业一本明明白白的账目。他说：“市场经济是法治经济，必须讲规则。只有让各类市场主体得到充分竞争、公平竞争，我们的市场和经济才能真正‘活’起来。”

　　李克强翻阅着手中的文件，不时点出其中一些“被取消的收费项目”说：“这些被清理的行政事业性收费，有多少是真正为了保证产品质量的？又有多少是保证公共安全的？相关部门是否应对仍然保留的涉企收费再进行一次必要的清理？”

　　“尤其是那些中介机构利用政府影响违规收费，必须坚决取消！”李克强厉声说道。

　　他坦言，清理涉企收费这项工作看似简单其实利益盘根错节，会动到不少机构的“奶酪”。“所以我们必须下决心压减政府行政性开支，用政府的‘紧日子’，真正换取企业和百姓的‘好日子’！”总理说，“要尽快推出制度性、管长远、见实效的清费举措，切实降低企业成本。优化实体经济环境。”

　　“今天就定下来，各部门要统一思想、负起责任，抓紧清理，尽早给百姓和企业一个满意的交代。到今年年底要让市场主体切实感受到清费成效！”李克强说。
     '''
    # windows = 3 # to specifiy the windows of coocurance matrix
    text3 = re.sub('\s+','',text1)
    # # docs = [e.strip() for e in text.splitlines()]
    # data = coocurance(text,windows=5)
    # # keywords
    # kw = textRank(data,d=0.75,kw_num=3)
    # result2 = textRank(data,d=0.75,kw_num=3,with_weight=True)
    # for text in docs:
    #     printDict(coocurance(text))

    #
    sent_graph = sentence_coocurance(text3)
    auto_abstract = abstractTextRank(sent_graph,sent_num=5,with_weight=True,d=0.3)
    # print '\n'.join(auto_abstract)
    for e,weight in auto_abstract:
        print e,weight