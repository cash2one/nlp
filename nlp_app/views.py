from __future__ import print_function

import json

from django.http import HttpResponse
from django.shortcuts import render

import zaber_nlp.posseg


def index(request):
    return render(request, 'index.html')


def add(request):
    s = request.POST['q']
    words = zaber_nlp.posseg.cut(s)
    word_list = []
    cate_list = []
    for word, flag in words:
        word_list.append(word)
        cate_list.append(flag)
    result = {'words': word_list, 'cate': list(set(cate_list))}
    return HttpResponse(json.dumps(result), content_type='application/json')
