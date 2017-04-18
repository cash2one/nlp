# -*- coding: utf-8 -*-
import codecs

if __name__ == '__main__':
    words = set()
    for line in open('origin/1.txt', 'rb'):
        tmp = line.strip().decode('utf-8')
        if tmp:
            words.add(tmp)
    words = sorted(list(words))
    file_object = codecs.open('origin/2.txt', 'w', "utf-8")
    for i in words:
        file_object.write(i + '\n')
    file_object.close()
