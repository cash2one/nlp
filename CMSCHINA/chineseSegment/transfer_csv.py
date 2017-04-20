#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys

import MySQLdb

sys.path.append("../preProcess")
reload(sys)
sys.setdefaultencoding('utf8')
from preProcess import PreProcess

prep = PreProcess()


def data2mysql_org(file_path):
    csv_reader = codecs.open(file_path, 'rb', 'utf-8')
    csv_list = []
    for row in csv_reader:
        line = row.split(',')
        csv_list.append(line)
    conn = MySQLdb.Connect(
        host='172.24.5.218',
        port=3306,
        db='text',
        user='crawl',
        passwd='crawl',
        charset='utf8')
    cursor = conn.cursor()
    for i in csv_list[1:]:
        # table.cell.value is unicode
        full_name = i[0]
        web_site = i[1]
        short_name = i[2]
        uc_no = str(i[3])
        register_no = i[3]
        sql = "insert into ORGANIZATION (FULL_NAME, WEB_SITE, SHORT_NAME, UC_NO, REGISTER_NO, submit_time) values(%s, %s, %s, %s, %s, now())"
        params = [full_name.strip(), web_site, short_name.strip(), uc_no, register_no]
        cursor.execute(sql, params)
    conn.commit()
    return


def data2mysql_pub(file_path):
    csv_reader = codecs.open(file_path, 'rb', 'utf-8')
    csv_list = []
    for row in csv_reader:
        line = row.split(',')
        csv_list.append(line)
    conn = MySQLdb.Connect(
        host='172.24.5.218',
        port=3306,
        db='text',
        user='crawl',
        passwd='crawl',
        charset='utf8')
    cursor = conn.cursor()
    for i in csv_list[1:]:
        market_code = i[0]
        market_desc = i[1]
        stock_code = i[2]
        stock_name = i[3]
        full_name = i[4]
        short_name = i[5]
        website = i[6]
        uc_no = i[7]
        sql = "insert into PUBLIC_COMPANY (MARKET_CODE, MARKET_DESC, STOCK_CODE, STOCK_NAME, FULL_NAME, SHORT_NAME, WEBSITE, UC_NO, submit_time) values(%s, %s, %s, %s, %s, %s, %s, %s, now())"
        params = [market_code, market_desc, stock_code, stock_name.strip(), full_name.strip(), short_name.strip(),
                  website, uc_no]
        cursor.execute(sql, params)
    conn.commit()
    return


if __name__ == "__main__":
    # data2mysql_org("or.xls")
    # data2mysql_pub("pu.xls")
    data2mysql_org("organization.csv")
    data2mysql_pub("public_company.csv")
