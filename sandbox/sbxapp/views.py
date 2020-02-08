import hashlib

from django.core import serializers
from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST

from .forms import ExampleForm, UploadFileForm, HashForm, CarForm
from .models import DtDemo, Hash, Car


def home(request):
    return render(request, 'sbxapp/home.html')


def hello(request, name=None):
    return render(request, 'sbxapp/hello.html', {'name': name})


def dt_all(request):
    dt_demos = DtDemo.objects.all()
    response = serializers.serialize('json', dt_demos)
    return HttpResponse(response, content_type='application/json')


def dt_all2(request):
    dt_demos = DtDemo.objects.values()  # model -> dict
    response = list(dt_demos)
    # return JsonResponse({'results': response})
    return JsonResponse(response, safe=False)  # listなどdict以外を返すとき


def form_example(request):
    """display form elements"""
    if request.method == 'POST':
        print(request.POST)
        form = ExampleForm(request.POST)
    else:
        form = ExampleForm()
    return render(request, 'sbxapp/form_example.html', {'form': form})


def handle_uploaded_file(f: UploadedFile):
    print("UploadedFile: name='{}', size={}, content_type={}".format(
        f.name, f.size, f.content_type))
    # ファイル移動


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('sbxapp:home')
    else:
        form = UploadFileForm()
    return render(request, 'sbxapp/upload.html', {'form': form})


def get_hashed_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def hashing_list(request):
    hash_list = Hash.objects.all().order_by('id')
    paginator = Paginator(hash_list, 5)
    page = request.GET.get('page')
    hashes = paginator.get_page(page)
    return render(request, 'hashing/hash_list.html', {'hashes': hashes})


def hash_detail(request, hash):
    hash = Hash.objects.get(hash=hash)
    return render(request, 'hashing/hash_detail.html', {'hash': hash})


def get_hash_ajax(request):
    text = request.GET['text']
    return JsonResponse({'hash': get_hashed_text(text)})


def create_hash(request):
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            text_hash = get_hashed_text(text)
            try:
                Hash.objects.get(hash=text_hash)
            except Hash.DoesNotExist:
                hash_obj = Hash()
                hash_obj.text = text
                hash_obj.hash = text_hash
                hash_obj.save()
            return redirect('sbxapp:hashing-detail', hash=text_hash)

    form = HashForm()
    return render(request, 'hashing/create_hash.html', {'form': form})


def car_list(request):
    """ / """
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'car_app/car_list.html', context)


class CarView(View):
    """
    /create/
    /<int:pk>/
    """
    form_class = CarForm
    model = Car

    def get(self, request, pk=None):
        if pk:  # show detail form
            car = get_object_or_404(self.model, pk=pk)
            form = self.form_class(instance=car)
            template_name = 'car_app/car_detail_form.html'
        else:  # show create form
            form = self.form_class()
            template_name = 'car_app/car_create_form.html'

        context = {'form': form}
        return render(request, template_name, context)

    def post(self, request, pk=None):
        if pk:  # update
            car = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=car)
        else:  # create
            form = self.form_class(request.POST)

        if form.is_valid():
            print(form.cleaned_data['name'])
            form.save()
        else:
            pass  # 省略
        return redirect('sbxapp:car-list')


@require_POST
def car_delete(request, pk):
    """ /<int:pk>/delete/ """
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('sbxapp:car-list')
