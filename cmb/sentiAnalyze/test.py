# encoding=utf-8
from senti import *


def main():
    model = Classify()
    ii = open('text', 'r')
    for line in ii:
        text_id, text = line.strip().split('\t')
        print text
        print model.clf3(text)
        print json.dumps(model.get_opinion_sentence(text), ensure_ascii=False)


if __name__ == '__main__':
    main()
