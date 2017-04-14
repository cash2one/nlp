#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd, MySQLdb, json, sys

sys.path.append("../preProcess")
from preProcess import PreProcess

prep = PreProcess()


def data2mysql_org(file_path):
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    conn = MySQLdb.Connect(
        host='172.24.5.218',
        port=3306,
        db='text',
        user='crawl',
        passwd='crawl',
        charset='utf8')
    cursor = conn.cursor()
    for i in xrange(1, nrows):
        # table.cell.value is unicode
        full_name = prep.normalize(table.cell(i, 0).value)
        web_site = prep.normalize(table.cell(i, 1).value)
        short_name = prep.normalize(table.cell(i, 2).value)
        uc_no = str(table.cell(i, 3).value)
        register_no = prep.normalize(table.cell(i, 4).value)
        sql = "insert into ORGANIZATION (FULL_NAME, WEB_SITE, SHORT_NAME, UC_NO, REGISTER_NO, submit_time) values(%s, %s, %s, %s, %s, now())"
        params = [full_name, web_site, short_name, uc_no, register_no]
        cursor.execute(sql, params)
    conn.commit()
    return


def data2mysql_pub(file_path):
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    conn = MySQLdb.Connect(
        host='172.24.5.218',
        port=3306,
        db='text',
        user='crawl',
        passwd='crawl',
        charset='utf8')
    cursor = conn.cursor()
    for i in xrange(1, nrows):
        market_code = prep.normalize(table.cell(i, 0).value)
        market_desc = prep.normalize(table.cell(i, 1).value)
        stock_code = prep.normalize(table.cell(i, 2).value)
        stock_name = prep.normalize(table.cell(i, 3).value)
        full_name = prep.normalize(table.cell(i, 4).value)
        short_name = prep.normalize(table.cell(i, 5).value)
        website = prep.normalize(table.cell(i, 6).value)
        uc_no = str(table.cell(i, 7).value)
        sql = "insert into PUBLIC_COMPANY (MARKET_CODE, MARKET_DESC, STOCK_CODE, STOCK_NAME, FULL_NAME, SHORT_NAME, WEBSITE, UC_NO, submit_time) values(%s, %s, %s, %s, %s, %s, %s, %s, now())"
        params = [market_code, market_desc, stock_code, stock_name, full_name, short_name, website, uc_no]
        cursor.execute(sql, params)
    conn.commit()
    return


if __name__ == "__main__":
    data2mysql_org("organization.xls")
    data2mysql_pub("public_company.xls")
