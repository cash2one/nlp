#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys, os, json, re
import jieba
import jieba.posseg as pg
import time

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append("../preProcess")
from preProcess import PreProcess

l_space_suffix = ["机场", "陆军基地", "海军基地", "空军基地", "小行星", "基地", "洼地", "公路", "教堂", "楼", "河畔", "花园", "公园", "湖畔", "湖", "寨",
                  "宫", "河段", "海滩", "景区", "海", "山", "社区", "镇", "省", "市", "县", "区", "街", "州", "地区", "自治区", "自治县", "省",
                  "市", "区", "县", "府", "州", "自治州", "乡", "路", "村", "港口", "城", "海港", "海湾", "海滩"]
l_org_suffix = ["一厂", "二厂", "三厂", "四厂", "五厂", "防疫站", "纺织厂", "丝织厂", "丝绸厂", "制品厂", "羽绒厂", "服装厂", "公司", "机械厂", "医院", "研究院",
                "研究所", "有限公司", "总局", "分局", "总厂", "分厂", "大学", "学院", "酒店", "会议中心", "中心", "分部", "宾馆", "交通部", "航天局", "分校",
                "联盟", "部", "厅", "局"]


class Segment(object):
    def __init__(self, pos_map, user_dict_path=None, stopwords=None):
        # 初始化预处理模块，传入用户自定义词典和停用词词典。停用词词典暂时不用保留。
        self.prep = PreProcess()
        self.d_pos_map = self.load_map(pos_map)
        self.user_dict = user_dict_path
        self.stopwords = stopwords
        # 上市公司实体名称词典
        self.s_pub_company = self.load_public_company()
        # 保存词性标注的结果
        self.l_res_pos = None
        # 传入的字符串
        self.string = None
        # 分词模式
        self.cut_mode = None
        if user_dict_path and isinstance(user_dict_path, list):
            for path in user_dict_path:
                jieba.load_userdict(path)
        return

    def load_map(self, pos_map):
        d_res = {}
        with open(pos_map) as f:
            for line in f:
                line = line.strip()
                k, v = line.split(" ")[0], line.split(" ")[1].decode("utf-8")
                d_res[k] = v
        return d_res

    def load_public_company(self):
        s_res = set()
        with open("./ner_dicts/public_company.txt") as f:
            for line in f:
                s_res.add(line.strip().decode("utf-8"))
        return s_res

    def pos_seg(self, string):
        # 分词模块
        self.string = self.prep.normalize(string).decode("utf-8")
        l_tmp = []
        flag_name = False
        l_orig_tuples = list(pg.cut(self.string))
        for idx in range(len(l_orig_tuples)):
            if l_orig_tuples[idx].word == u" ":
                continue
            next_word = ''
            if idx + 1 < len(l_orig_tuples):
                next_word = l_orig_tuples[idx + 1]
            # 合并人名
            if l_orig_tuples[idx].word == u"·" and len(l_tmp) > 0 and 'nr' in l_tmp[-1][1] and 'nr' in next_word.flag:
                flag_name = True
                l_tmp[-1][0] += u"·"
                continue
            if flag_name and len(l_tmp):
                flag_name = False
                l_tmp[-1][0] += l_orig_tuples[idx].word
                continue
            # 合并数词+时间词
            if l_orig_tuples[idx].flag == 't' and len(l_tmp) > 0 and l_tmp[-1][1] == 'm':
                l_tmp[-1][0] += l_orig_tuples[idx].word
                continue
            # 合并时间词+方位词
            if l_orig_tuples[idx].flag == 'f' and len(l_tmp) > 0 and l_tmp[-1][1] == 't':
                l_tmp[-1][0] += l_orig_tuples[idx].word
                continue
            # 合并数词和数词
            if l_orig_tuples[idx].flag == 'm' and len(l_tmp) > 0 and l_tmp[-1][1] == 'm':
                l_tmp[-1][0] += l_orig_tuples[idx].word
                continue
            l_tmp.append([l_orig_tuples[idx].word, l_orig_tuples[idx].flag])
        self.l_res_pos = l_tmp
        l_tmp = [[item[0].encode("utf-8"), self.d_pos_map[item[1]].encode("utf-8")] for item in l_tmp]
        # 删除自定义词典里面的词语
        t1 = time.time()
        for path in self.user_dict:
            with open(path) as f:
                for line in f:
                    word = line.strip().split(" ")[0]
                    jieba.del_word(word)
        t2 = time.time()
        # print t2 - t1
        return l_tmp

    def ner_recog(self, string):
        # 命名实体是在词性标注的基础上做的，所以后续根据接口来决定要不要在词性标注里面将结果存进类私有变量里面。
        if not self.l_res_pos:
            return ""
        l_ner = []
        l_ner += self.search_nr()
        l_ner += self.search_ns()
        l_ner += self.search_nt()
        l_ner += self.search_t()
        l_ner += self.search_nz()
        l_ner += self.search_pub_com()
        l_ner += self.search_other_ner()
        l_ner = [(item[0].encode("utf-8"), self.d_pos_map[item[1]].encode("utf-8")) for item in l_ner]
        return list(set(l_ner))

    def search_nr(self):
        l_tmp = []
        for item in self.l_res_pos:
            item = tuple(item)
            if 'nr' in item[1] and len(l_tmp) and 'nr' in l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'nr')
            else:
                l_tmp.append(item)
        l_res = []
        for item in l_tmp:
            if 'nr' in item[1]:
                l_res.append(item)
        return l_res

    def search_ns(self):
        l_tmp = []
        for item in self.l_res_pos:
            item = tuple(item)
            if item[0].encode("utf-8") in l_space_suffix and len(l_tmp) and l_tmp[-1][1].startswith('n'):
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'ns')
            elif 'ns' in item[1] and len(l_tmp) and 'ns' in l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'ns')
            elif item[1] == 'f' and len(l_tmp) and 'ns' in l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'ns')
            else:
                l_tmp.append(item)
        l_res = []
        for item in l_tmp:
            if 'ns' in item[1]:
                l_res.append(item)
        return l_res

    def search_nt(self):
        l_tmp = []
        for item in self.l_res_pos:
            item = tuple(item)
            if 'nt' in item[1] and len(l_tmp) and 'nt' in l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'nt')
            else:
                l_tmp.append(item)
        l_temp = []
        # 回溯找ns + nxx ... + nt后缀词的模式，如美国康奈尔大学
        for idx in xrange(len(l_tmp)):
            item = l_tmp[idx]
            if item[0].encode("utf-8") in l_org_suffix:
                i = 1
                tmp = item[0]
                # 以当前词为基准进行回溯
                while i <= 3 and i <= idx:
                    # 必须是名词性质才会进行回溯
                    if not l_tmp[idx - i][1].startswith("n"):
                        l_temp.append(item)
                        break
                    else:
                        if 'ns' not in l_tmp[idx - i][1]:
                            tmp = l_tmp[idx - i][0] + tmp
                            i += 1
                        else:
                            tmp = l_tmp[idx - i][0] + tmp
                            # 找到了ns，把之前的删掉
                            for j in xrange(i):
                                l_temp.pop()
                            l_temp.append((tmp, 'nt'))
                            break
            else:
                l_temp.append(item)
        l_res = []
        for item in l_temp:
            if 'nt' in item[1]:
                l_res.append(item)
        return l_res

    def search_t(self):
        l_tmp = []
        for item in self.l_res_pos:
            item = tuple(item)
            if 't' == item[1] and len(l_tmp) and 't' == l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 't')
            else:
                l_tmp.append(item)
        l_res = []
        for item in l_tmp:
            if 't' in item[1]:
                l_res.append(item)
        return l_res

    def search_nz(self):
        l_tmp = []
        for item in self.l_res_pos:
            item = tuple(item)
            if 'nz' in item[1] and len(l_tmp) and 'nz' in l_tmp[-1][1]:
                l_tmp[-1] = (l_tmp[-1][0] + item[0], 'nz')
            else:
                l_tmp.append(item)
        l_res = []
        for item in l_tmp:
            if 'nz' in item[1]:
                l_res.append(item)
        return l_res

    def search_pub_com(self):
        l_res = []
        string = self.string
        for item in self.s_pub_company:
            if item in string:
                string = string.replace(item, "")
                l_res.append((item, 'company'))
        self.string = string
        return l_res

    def search_other_ner(self):
        t1 = time.time()
        l_res = []
        string = self.string
        # 手机号码
        phone_pat = ur"1\d{10}"
        # qq号码
        qq_pat = ur"\d{6,13}"
        # email
        mail_pat = ur"\w{1,15}@\w{2,10}.com"
        # 身份证号码
        id_pat = ur"\d{18}"
        # 银行账户
        bank_pat = ur"\d{16}"
        # 车牌号
        car_pat = ur"\W[A-Z]\d{5}"

        l_id = re.findall(id_pat, string)
        # 将找到的身份证号从原文中删除，不影响后续手机号码，QQ号码的判断。
        for item in l_id:
            string = string.replace(item, "")
        l_bank = re.findall(bank_pat, string)
        # 删除银行账号
        for item in l_bank:
            string = string.replace(item, "")
        l_qq = re.findall(qq_pat, string)
        # 删除qq账号
        for item in l_qq:
            if len(item) > 11:
                string = string.replace(item, "")
        l_phone = re.findall(phone_pat, string)
        l_mail = re.findall(mail_pat, string)
        l_car = re.findall(car_pat, string)

        l_res += [(item, 'id') for item in l_id]
        l_res += [(item, 'bank') for item in l_bank]
        l_res += [(item, 'qq') for item in l_qq]
        l_res += [(item, 'phone') for item in l_phone]
        l_res += [(item, 'email') for item in l_mail]
        l_res += [(item, 'car') for item in l_car]
        t2 = time.time()
        # print t2 - t1
        return l_res


if __name__ == "__main__":
    seg = Segment("pos_map.txt", ["E:/PycharmProjects/nlp/CMSCHINA/keywordsExtract/user_dict.txt"])
    # l_pos_seg = seg.pos_seg("美国格林大学乔治?克林顿决定出访中国， 习近平将迎接他。他们将在1991年2月3日下午五点左右会面。我的电话号码是13807025737，QQ号是3356701943，email是sgyjkl_34@126.com，备用邮箱是30807033@qq.com，身份证号是370401198912150427，银行账号是6214342578651989，车牌号是冀J33455")
    # print " ".join([item[0].decode("utf-8") + "/" + item[1].decode("utf-8") for item in l_pos_seg])
    # l_ner_recog = seg.ner_recog("美国格林大学乔治?克林顿决定出访中国， 习近平将迎接他。他们将在1991年2月3日下午五点左右会面。我的电话号码是13807025737，QQ号是3356701943，email是sgyjkl_34@126.com，备用邮箱是30807033@qq.com，身份证号是370401198912150427，银行账号是6214342578651989，车牌号是冀J33455")
    # print " ".join([item[0].decode("utf-8") + "/" + item[1].decode("utf-8") for item in l_ner_recog])
