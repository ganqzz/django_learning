from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def top(request):
    return render(request, 'top.html')


def trailing_slash(request):
    return HttpResponse('<h2>Try access to the URL with or without trailing slash.</h2>')


@csrf_exempt
def params(request):
    if request.method =='GET':
        res = str(dict(request.GET))
    elif request.method =='POST':
        res = str(dict(request.POST))
    else:
        res = 'GET/POST method only'
    return HttpResponse(res)
