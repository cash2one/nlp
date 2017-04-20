# encoding=utf-8
from gensim.models import word2vec
import time
import traceback


def returnNone(func):
    # return func
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # traceback.print_exc()
            return []

    return wrapper


def listlist2list(listlist):
    rval = reduce(lambda x, y: x + y, listlist, [])
    return rval


class SynonymModel():
    def __init__(self, path):
        self.synonym_words = self.read(path)

    def read(self, path):
        rval = {}
        ii = open(path, 'r')
        for line in ii:
            try:
                word, words_list = line.strip().split('\t')
                words_list = words_list.split(',')
                rval[word] = words_list
            except:
                pass
        # print line
        return rval

    @returnNone
    def synonym(self, word):
        return self.synonym_words[word]


class TycclModel():
    def __init__(self, path):
        self.tag2wordslist, self.tag_type, self.word2tag, self.tag2neartag = \
            self.read_tyccl(path)

    def read_tyccl(self, path):
        a = open(path, 'r').readlines()
        tag_type = {}
        tag2wordslist = {}
        word2tag = {}
        word2neartag = {}
        tag2neartag = {}
        before_tag = None
        tag_list = []
        for line in a:
            line = line.strip()
            if '=' in line:
                tpe = '='
            elif '@' in line:
                tpe = '@'
            else:
                tpe = '#'
            line = line.replace('@', '=').replace('#', '=')
            tag, words_list = line.split('=')
            words_list = words_list.strip().split(' ')
            tag2wordslist[tag] = words_list
            for word in words_list:
                if word not in word2tag: word2tag[word] = []
                word2tag[word].append(tag)
            tag_type[tag] = tpe
            if before_tag == None or tag[0:5] == before_tag[0:5]:
                tag_list.append(tag)
            else:
                if len(tag_list) <= 6:
                    for t in tag_list:
                        if t not in tag2neartag:
                            tag2neartag[t] = []
                        tag2neartag[t] += tag_list
                else:
                    # print len(tag_list)
                    k = 0
                    for t in tag_list:
                        tag2neartag[t] = tag_list[max(0, k - 1):min(len(tag_list) - 1, k + 2)]
                        k = k + 1

                tag_list = [tag]
            before_tag = tag
        for t in tag_list:
            tag2neartag[t] = tag_list
        return tag2wordslist, tag_type, word2tag, tag2neartag

    @returnNone
    def synonym(self, word, use_mean_group=False):
        tags = [t for t in self.word2tag[word] if self.tag_type[t] != '#']
        rval = []
        for tag in tags:
            rval = rval + [self.tag2wordslist[tag]]
        if not use_mean_group:
            rval = listlist2list(rval)
        return rval

    @returnNone
    def nearsynonym(self, word, use_mean_group=False):

        tags = []
        for t in self.word2tag[word]:
            if self.tag_type[t] == '#':
                tags += [[t]]
            else:
                tags += [self.tag2neartag[t]]
        rval = []
        for sub_tags in tags:
            sub_list = []
            for tag in sub_tags:
                sub_list = sub_list + [(x, 1) for x in self.tag2wordslist[tag]]
            rval = rval + [sub_list]
        if not use_mean_group:
            rval = listlist2list(rval)
        return rval


def read_qiyi(qiyipath):
    ii = open(path, 'r')
    word2qiyi = {}
    for line in ii:
        word, wlist = line.strip().split('\t')
        wlist = wlist.split('\t')
        word2qiyi[word] = wlist
    return word2qiyi


class WikiRedirectModel():
    def __init__(self, path, qiyi_path=None):
        self.word2tag, self.tag2wordslist = self.read(path)
        if qiyi_path != None:
            self.word2qiyi = read_qiyi(qiyi_path)

    def read(self, path):
        # TODO 处理 同名tag,消歧等
        ii = open(path, 'r')
        word2tag = {}
        tag2wordslist = {}
        for line in ii:
            w1, w2 = line.strip().split('\t')
            if '/' in w1 or '/' in w2: continue
            if w1 not in word2tag: word2tag[w1] = set([w1])
            if w2 not in word2tag: word2tag[w2] = set([w2])
            word2tag[w1].add(w2)  # TODO 没必要啊
            if w2 not in tag2wordslist:
                tag2wordslist[w2] = set([w2])
            tag2wordslist[w2].add(w1)
        for word in word2tag:
            if len(word2tag[word]) >= 3:
                pass
        # print word,'\t'.join(list(word2tag[word]))
        for tag in tag2wordslist:
            tag2wordslist[tag] = list(tag2wordslist[tag])
        return word2tag, tag2wordslist

    @returnNone
    def synonym(self, word, use_mean_group=False):
        # TODO 有问题
        # 这里要group， 就要对输入消歧
        tags = self.word2tag[word]
        # tags=[word]+self.word2qiyi[word]
        # tags=self.word2tag[word]
        rval = []
        for tag in tags:
            rval += [self.tag2wordslist[tag]]
        if not use_mean_group:
            rval = listlist2list(rval)
        return rval


class WikicategoryModel():
    def __init__(self, path, word2tag):
        # 为什么iphone没有？
        # 考虑消歧
        # 考虑英文数据库
        # 先加入重定向
        self.word2similar = self.read(path)
        self.word2name = word2tag
        # self.similar_=

    def read(self, path):
        ii = open(path, 'r')
        rval = {}
        for line in ii:
            try:
                w1, cat_num, words_list, p_list = line.strip().split('\t')
                cat_num = int(cat_num)
                words_list = words_list.split(' ')
                p_list = [int(x) * 1.0 / cat_num for x in p_list.split(' ')]
                rval[w1] = zip(words_list, p_list)
            except:
                pass
        # print line
        return rval

    @returnNone
    def nearsynonym(self, word, topn=50, use_mean_group=False):

        if word in self.word2name:
            rval = [self.word2similar[w] for w in self.word2name[word]]
        else:
            rval = [self.word2similar[word]]
        if not use_mean_group:
            rval = listlist2list(rval)
        return rval


class Word2vecModel():
    def __init__(self, path):
        self.model = word2vec.Word2Vec.load_word2vec_format(path, binary=False)

    @returnNone
    def nearsynonym(self, word, topn=50, use_mean_group=False):
        word = word.decode('utf-8')
        rval = []
        if word not in self.model:
            return []
        similar = self.model.most_similar(word, topn=topn)
        for ww, p in similar:
            rval.append((ww.encode('utf-8'), p))
        return rval


class Model():
    def __init__(self, synonym_path, tyccl_path, wikiredirect_path, wikicategory_path, word2vec_path,
                 only_synonym=False):
        print 'load 1.1...'
        self.synonym_model = SynonymModel(synonym_path)
        print 'load 1.2...'
        synonym_path2 = synonym_path + '_extended'
        self.synonym_model2 = SynonymModel(synonym_path2)
        print 'load 2...'
        self.tyccl_model = TycclModel(tyccl_path)
        print 'load 3...'
        self.wikiredirect_model = WikiRedirectModel(wikiredirect_path)
        if only_synonym:
            return
        print 'load 4...'
        self.word2vec_model = Word2vecModel(word2vec_path)
        print 'load 5...'
        f = self.category_model = WikicategoryModel(wikicategory_path, self.wikiredirect_model.word2tag)

    @returnNone
    def similar(self, w1, w2):
        return 'Not imPlemented Error'
        wl1 = self.synonym(w1)
        wl2 = self.synonym(w2)
        if w1 == w2 or w2 in wl1 or w1 in wl2:
            return 1
        return

    @returnNone
    def synonym(self, word, mode='auto', use_means_group=False):
        split = 'split' in mode
        auto = 'auto' in mode
        extended = 'extended' in mode and not 'only_extended' in mode
        only_extended = 'only_extended' in mode
        if auto:
            rval = {'synonym': self.synonym_model.synonym(word),
                    'tyccl': self.tyccl_model.synonym(word),
                    'wiki': self.wikiredirect_model.synonym(word)}
        elif only_extended:
            rval = {'synonym': list(set(self.synonym_model2.synonym(word)) - \
                                    set(self.synonym_model.synonym(word)))}
        elif extended:
            rval = {'synonym': self.synonym_model.synonym(word),
                    'tyccl': self.tyccl_model.synonym(word),
                    'wiki': self.wikiredirect_model.synonym(word)}
        if not split:
            rval2 = []
            for name in rval:
                rval2 += rval[name]
            rval = [w for w in list(set(rval2)) if w != word]
        return rval

    @returnNone
    def nearsynonym(self, word, maxn=50, mode='auto', use_means_group=False):
        '''
        mode could be 'tyccl+word2vec', 'wiki'
        tyccl
        '''
        # TODO: 输入一个list
        synonym_words = self.synonym(word)
        rval_list = []
        name_list = []
        use_wiki = 'wiki' in mode or 'auto' in mode
        use_tyccl = 'tyccl' in mode or 'auto' in mode
        use_w2v = 'word2vec' in mode or 'auto' in mode
        split = 'split' in mode

        if use_means_group:
            raise
        if use_tyccl:
            rval_list.append(self.tyccl_model.nearsynonym(word))
            name_list.append('tyccl')
        if use_w2v:
            rval_list.append(self.word2vec_model.nearsynonym(word, topn=maxn))
            name_list.append('word2vec')
        if use_wiki:
            rval_list.append(self.category_model.nearsynonym(word, topn=maxn))
            name_list.append('wiki')

        def process(seq):  # 去重并且保持顺序
            seen = set()
            seen_add = seen.add
            rval = [x for x in seq if not (x in seen or seen_add(x))]
            rval = [w for w, p in rval if w not in synonym_words and w != word]
            rval = rval[:maxn]
            return rval

        if split:
            rval = [process(x) for x in rval_list]
            rval = {x: y for x, y in zip(name_list, rval)}
        else:
            rval = listlist2list(rval_list)
            rval = sorted(rval, key=lambda x: x[1], reverse=True)
            rval = process(rval)

        return rval


if __name__ == '__main__':
    model = Model('synonym.txt', 'tyccl.txt', 'redirect.txt', 'wiki_similar.txt', 'vec.txt')
    while True:
        word = raw_input('Enter word:')
        words0 = model.synonym(word)
        print 'synonym:\t' + ' '.join(words0)
        words1 = model.nearsynonym(word)
        print 'nearsynonym:\t' + ' '.join(words1)
