from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from .models import DtDemo


def home(request):
    return render(request, 'home.html')


def dt_all(request):
    dt_demos = DtDemo.objects.all()
    response = serializers.serialize('json', dt_demos)
    return HttpResponse(response, content_type='application/json')


def dt_all2(request):
    dt_demos = DtDemo.objects.values()  # model -> dict
    response = list(dt_demos)
    # return JsonResponse({'results': response})
    return JsonResponse(response, safe=False)
