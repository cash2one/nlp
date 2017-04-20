# encoding=utf-8
import json
# import readline
from gen.opinion.Opinion import Client
from bfd.harpc.common import config
from bfd.harpc import client
import sys

if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/client.conf.' + branch
    conf = config.Config(conf_path)
    manager = client.Client(Client, conf)
    client_ = manager.create_proxy()

    text = '京东好。淘宝好。马云傻逼。'
    objects = json.dumps({'电商': ['京东', '淘宝'], '马云': ['马云']})
    objects_updated = False
    print client_.analysis(text, text, objects, False)
    while True:
        title = raw_input('Enter title')
        content = raw_input('Enter content')
        o = raw_input('Enter objects')
        names = raw_input('Enter names').split()
        objects = json.dumps({o: names})
        objects_updated = False

        print client_.analysis(title, content, objects, False)
