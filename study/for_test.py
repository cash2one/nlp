# -*- coding: utf-8 -*-
import codecs

if __name__ == '__main__':
    words1 = set()
    for line in open('organizat1ion.txt', 'rb'):
        tmp = line.strip().decode('utf-8')
        sp = tmp.split(' ')
        if tmp:
            print sp
            # words1.add(sp[0])
            # f = codecs.open('origin/aa', 'w', 'utf-8')
            # for i in sorted(list(words1)):
            #     f.write(i + ' 100 jr' + '\n')
            # f.close()
            # words2 = set()
            # for line in open('origin/hx1.txt', 'rb'):
            #     tmp = line.strip().decode('utf-8')
            #     sp = tmp.split(' ')
            #     if tmp:
            #         words2.add(sp[0])
            # f = codecs.open('origin/hx1.txt', 'w', 'utf-8')
            # for i in sorted(list(words2)):
            #     f.write(i + '\n')
            # f.close()
            # words3 = set()
            # for line in open('origin/hx2.txt', 'rb'):
            #     tmp = line.strip().decode('utf-8')
            #     sp = tmp.split(' ')
            #     if tmp:
            #         words3.add(sp[0])
            # f = codecs.open('origin/hx2.txt', 'w', 'utf-8')
            # for i in sorted(list(words1)):
            #     f.write(i + '\n')
            # f.close()
            # f = codecs.open('origin/jr.txt', 'w', 'utf-8')
            # for i in sorted(list(words1 | words2 | words3)):
            #     f.write(i + ' 100 jr' + '\n')
            # f.close()
