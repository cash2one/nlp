import time
import sys
sys.path.append("../")
import zaberFenci
zaberFenci.initialize()

url = sys.argv[1]
content = open(url,"rb").read()
t1 = time.time()
words = "/ ".join(zaberFenci.cut(content))

t2 = time.time()
tm_cost = t2-t1

log_f = open("1.log","wb")
log_f.write(words.encode('utf-8'))
log_f.close()

print('cost ' + str(tm_cost))
print('speed %s bytes/second' % (len(content)/tm_cost))

