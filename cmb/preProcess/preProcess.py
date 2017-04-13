#!/usr/bin/env python
# -*- coding:utf-8 -*-

import chardet
from langconv import *


class PreProcess(object):
    def __init__(self):
        return

    def check_coding(self, string):
        # 检测编码格式
        if isinstance(string, unicode):
            return 'unicode'
        elif isinstance(string, str):
            # print chardet.detect(string)
            if chardet.detect(string)['encoding'] == 'utf-8':
                return 'utf-8'
            elif chardet.detect(string)['encoding'] == 'GB2312':
                return 'gbk'
            else:
                print "encoding must be utf-8 or gbk."
                return
        else:
            print "pls input an string format data or unicode."
            return

    def traditional2simple(self, string):
        # 必须为utf-8或者unicode
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        # 结果是unicode
        return Converter('zh-hans').convert(string)

    def simple2traditional(self, string):
        # 必须为utf-8或者unicode
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        # 结果是unicode
        return Converter('zh-hant').convert(string)

    def full2half(self, string):
        # 全角转半角
        res_str = ""
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        for char in string:
            encode_char = ord(char)
            if encode_char == 12288:
                encode_char = 32
            elif encode_char >= 65281 and encode_char <= 65374:
                encode_char -= 65248
            res_str += unichr(encode_char)
        return res_str

    def normalize(self, string):
        # 将编码、全半角、繁简体归一化成utf-8，半角，简体。
        # 编码变utf-8
        if not len(string):
            return ""
        if self.check_coding(string) == 'unicode':
            string = string.encode("utf-8")
        elif self.check_coding(string) == 'gbk':
            string = string.decode("gbk").encode("utf-8")
        else:
            pass
        # 全角转半角
        string = self.full2half(string)
        # 繁体转简体
        string = self.traditional2simple(string).encode("utf-8")
        return string


if __name__ == "__main__":
    prep = PreProcess()
    print prep.check_coding("纯粹是微家连锁店客服".decode("utf-8").encode("gbk"))
    print prep.traditional2simple(
        """
        # 簡繁體在線轉換工具 v1.0
        # 簡體中文、繁體中文 只對單個的文字進行轉換
        # 大陸簡體、港澳繁體、台灣正體、馬新簡體 都會對習慣用語進行替換
        """)
    print prep.normalize("""
    簡繁體在線轉換工具 ｖ１.０
    """
                         )
