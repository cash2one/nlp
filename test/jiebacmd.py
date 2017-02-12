'''
usage example (find top 100 words in abc.txt):

cat abc.txt | python zaberFencicmd.py | sort | uniq -c | sort -nr -k1 | head -100


'''

from __future__ import unicode_literals
import sys
sys.path.append("../")

import zaberFenci

default_encoding='utf-8'

if len(sys.argv)>1:
    default_encoding = sys.argv[1]

while True:
    line = sys.stdin.readline()
    if line=="":
        break
    line = line.strip()
    for word in zaberFenci.cut(line):
        print(word)


