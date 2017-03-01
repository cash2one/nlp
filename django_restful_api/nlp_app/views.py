import json

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')


def add(request):
    if request.is_ajax():
        ajax_string = 'ajax request: '
        print ajax_string
    print request
    a = int(request.POST['a'])
    b = int(request.POST['b'])

    result = {'result': str(a + b)}
    return HttpResponse(json.dumps(result), content_type='application/json')
