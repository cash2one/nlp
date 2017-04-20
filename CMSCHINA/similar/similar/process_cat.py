# encoding=utf-8
from similar import returnNone
import time
import multiprocessing as mp
import traceback


def expand_cats(tree, cats):
    todo = cats
    todo_set = set(cats)
    start = 0
    while start < len(todo):
        cat = todo[start]  # page与cat有可能同名
        # if depth>=1:continue
        if cat in tree:
            for w in tree[cat]:
                if w in tree and w not in todo_set:
                    print cat, w
                    todo.append(w)
                    todo_set.add(w)
        start += 1
    return todo_set


def sorted_topn(a, topn, key=lambda x: len(x[1]), value=lambda x: x[0], page_set=None):
    a = [i for i in a if i[0] in page_set]
    if len(a) == 0: return []
    keys = map(key, a)
    mmin, mmax = min(keys), max(keys)
    '''这个代码有问题
    n=mmax-mmin+1
    blocks=[set([]),]*n
    for i in range(len(a)):
        j=key(a[i])-mmin
        blocks[j].add(i)
    fset=set([])
    for j in range(len(blocks))[::-1]:
        print j
        fset|=blocks[j]
        for i in blocks[j]:
            print 'add',i,keys[i],
    if len(fset)>=topn:break
    b=[a[i] for i in fset]
    print mmax,mmin,j
    if j==len(blocks)-1:return b[0:topn] 
    '''
    blocks = {}
    for i in range(len(a)):
        j = keys[i]
        if j not in blocks:
            blocks[j] = []
        blocks[j].append(a[i])
    b = []
    while len(b) < topn and mmax >= mmin:
        if mmax not in blocks:
            mmax -= 1
            continue
        b = b + blocks[mmax]
        mmax = mmax - 1
    rval = b[0:topn]
    # rval=map(value,rval)
    return rval


class WikicategoryModel():
    def __init__(self, path):
        # 为什么iphone没有？
        # 考虑消歧
        # 考虑英文数据库
        self.word2cats, self.cat2words, self.page_set = self.read(path)
        # self.similar_=

    def read(self, path):
        ii = open(path, 'r')
        word2cats = {}
        cat2words = {}
        page_set = set([])
        for line in ii:
            line = line.strip()
            w1, w2, typ = line.strip().split('\t')
            if typ == 'page' and w1 not in page_set:
                page_set.add(w1)
            if w1 not in word2cats:
                word2cats[w1] = set([])
            word2cats[w1].add(w2)
            if w2 not in cat2words:
                cat2words[w2] = set([])
            cat2words[w2].add(w1)
        # self.filter_cats=expand_cats(cat2words, ['隐藏分类','追踪分类'])#TODO：考虑子分类与其他分类
        # self.filter_cats=set([cat for cat in self.filter_cats if word2cats[cat] <= self.filter_cats])
        self.filter_cats = set([cat for cat in cat2words['隐藏分类'] | cat2words['追踪分类'] if '作品' not in cat])
        oo = open('filter_cats', 'w')
        for w in self.filter_cats:
            oo.write(w + '\n')
        oo.close()
        # self.filter_cats=[w for w in self.filter_cats \
        #    if ('条目' in w or '维基' in w or '页面' in w)]
        # self.nofilter_cats=expand_cats(cat2words, ['页面分类'])

        # print 'nofilter_cats num=',len(self.nofilter_cats)
        print 'filter_cats num=', len(self.filter_cats)
        print 'all_cats=', len(cat2words)
        print 'all_words', len(word2cats)
        # self.filter_cats-=self.nofilter_cats
        # print 'filter_cats2 num=',len(self.filter_cats)
        for word in word2cats:
            word2cats[word] = word2cats[word] - self.filter_cats
        return word2cats, cat2words, page_set

    def similar(self, w1, w2):  # 需要离线把w topn 算好，放到一个文件里
        cats1 = self.word2cats[w1]
        cats2 = self.word2cats[w2]
        # print 'union cats:', '\t'.join(list(set(cats1) & set(cats2)))
        return cats1 & cats2

    # @returnNone
    def nearsynonym(self, word, topn=50):
        cats = self.word2cats[word]
        # print 'tags:', '\t'.join(list(cats))
        rval = {}
        for cat in cats:
            words = self.cat2words[cat]
            now = time.time()
            for word_ in words:
                if word_ not in rval:
                    rval[word_] = self.similar(word, word_)
        topn = min(topn, len(rval))
        rval = sorted_topn(list(rval.iteritems()), topn, page_set=self.page_set)
        # print 'rval:'
        # for x in rval:
        # print x[0]+'\t'+','.join(list(x[1]))
        rval = [w for w, p in rval if w != word]
        # for word_ in rval:print len(self.similar(word,word_))
        return rval


a = WikicategoryModel('categorylinks.txt')


def process(word):
    print '1'
    try:
        return a.nearsynonym(word, 200)
    except:
        traceback.print_exc()
        return []


if __name__ == '__main__':
    oo = open('wiki_similar.txt', 'w')
    words = [w for w in a.word2cats if 'PRC_admin' not in w]
    pool = mp.Pool(20)
    while words:
        n = min(200, len(words))
        tasks = words[0:n]
        words = words[n:]
        rval = pool.map(process, tasks)
        for i in range(len(tasks)):
            if rval[i] == []: continue
            oo.write(tasks[i] + '\t' + ' '.join(rval[i]) + '\n')
    oo.close()
