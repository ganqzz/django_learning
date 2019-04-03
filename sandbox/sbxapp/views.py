from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from .forms import ExampleForm, UploadFileForm
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


def form_example(request):
    form = ExampleForm()
    return render(request, 'form_example.html', {'form': form})


def handle_uploaded_file(f: UploadedFile):
    print(f.name)
    print(f.size)
    print(f.content_type)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('sbxapp:home')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
