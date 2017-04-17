# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def read_stopwords(infile):
    st_stopwords = set()
    for line in open(infile, 'rb'):
        tmp = line.strip().decode('utf-8')
        if tmp:
            st_stopwords.add(tmp)
    return st_stopwords


def load_user_dict(infile):
    """
    加载新词词库，提高分词准确率

    """
    ud_userdicts = set()
    for line in open(infile, 'rb'):
        tmp = line.strip().decode('utf-8')
        if tmp:
            ud_userdicts.add(tmp)
    return ud_userdicts


def read_public_company():
    com_list = []
    # db = MySQLdb.Connect(
    #     host='172.24.5.218',
    #     port=3306,
    #     db='text',
    #     user='crawl',
    #     passwd='crawl',
    #     charset='utf8')
    # cursor = db.cursor()
    # # SQL 查询语句
    # sql = "SELECT FULL_NAME,STOCK_NAME FROM PUBLIC_COMPANY LIMIT 10"
    # try:
    #     # 执行SQL语句
    #     cursor.execute(sql)
    #     # 获取所有记录列表
    #     results = cursor.fetchall()
    #     for row in results:
    #         FULL_NAME = row[0]
    #         STOCK_NAME = row[1]
    #         # 打印结果
    #         com_list.append([FULL_NAME,STOCK_NAME])
    # except:
    #     print "Error: unable to fecth data"
    # # 关闭数据库连接
    # db.close()
    stock_list = [u'蓝黛传动', u'锦龙股份']
    full_list = [u'重庆蓝黛动力传动机械股份有限公司', u'广东锦龙发展股份有限公司']
    return stock_list, full_list


def load_wd_df(df_file):
    wd_df = {}
    for line in open(df_file):
        l_data = line.split('\t')
        wd = l_data[0].strip()
        if not wd:
            continue
        wd = unicode(wd, 'utf-8')
        wd_df[wd] = float(l_data[1])
    return wd_df


def readfile(in_path):
    '''

    :param in_path: 测试文件，是一篇的新闻，第一行是title，其他行是content

    :return: 两个字符串，title, content
    '''
    hl = open(in_path)
    l_lines = [line.strip('\n') for line in hl.readlines()]
    title = ''
    content = ''
    if l_lines:
        title = l_lines[0]
    content = ' '.join(l_lines)
    return title, content
