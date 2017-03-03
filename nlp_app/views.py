from __future__ import print_function

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from zaber_nlp import posseg, analyse


# def index(request):
#     return render(request, 'index.html', )


@csrf_exempt
def word_seg(request):
    result = {}
    if request.method == 'POST':
        s = request.POST['q']
        words = posseg.cut(s)
        word_list = []
        cate_list = []
        for word, flag in words:
            word_list.append(word)
            cate_list.append(flag)
        result = {'words': word_list, 'category': list(set(cate_list))}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def key(request):
    result = {}
    if request.method == 'POST':
        s = request.POST['q']
        words = analyse.Text_Rank(s, withWeight=True, allowPOS='n')
        key_list = []
        print(words)
        for word, weight in words:
            print(word, weight)
            key_list.append([word, weight])
        result = {'task_pd': key_list}
    return HttpResponse(json.dumps(result), content_type='application/json')
