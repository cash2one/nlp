# -*- coding: utf-8 -*-
import codecs

if __name__ == '__main__':
    words1 = set()
    for line in open('origin/hx1.txt', 'rb'):
        tmp = line.strip().decode('utf-8')
        sp = tmp.split(' ')
        if tmp:
            words1.add(sp[0])
    words2 = set()
    for line in open('origin/hx2.txt', 'rb'):
        tmp = line.strip().decode('utf-8')
        sp = tmp.split(' ')
        if tmp:
            words2.add(sp[0])

    f = codecs.open('origin/jr.txt', 'w', 'utf-8')
    for i in sorted(list(words1 | words2)):
        f.write(i + ' 100 jr' + '\n')
    f.close()
