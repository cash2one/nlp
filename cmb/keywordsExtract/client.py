# encoding=utf-8
import json
from gen.keywords.KeywordsService import Client
from bfd.harpc.common import config
from bfd.harpc import client
import sys

if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/client.conf.' + branch
    conf = config.Config(conf_path)
    manager = client.Client(Client, conf)
    client_ = manager.create_proxy()

    word = """１月１５日至１８日，国家主席习近平将对瑞士进行国事访问并赴达沃斯出席世界经济论坛２０１７年年会，其间将访问联合国日内瓦总部、世界卫生组织和国际奥委会。深化中瑞伙伴关系，带动中欧整体合作；提振世界经济信心，推动全球治理变革。习主席新年首访，立足一国，面向欧洲和全球，分享治理智慧，彰显大国担当，为世界注入和平发展、合作共赢的中国“正能量”。"""
    word = "《测试书名》"
    print client_.get_keywords(word, 3)
