import hashlib

from django.core import serializers
from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.decorators.http import require_POST

from .forms import ExampleForm, UploadFileForm, HashForm, CarForm
from .models import DtDemo, Hash, Car, Post


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


# --- Car app

def car_list(request):
    """ / """
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'car_app/car_list.html', context)


def car_detail(request, pk):
    """ /<int:pk>/ """
    car = get_object_or_404(Car, pk=pk)
    context = {'car': car}
    return render(request, 'car_app/car_detail.html', context)


class CarEditView(View):
    """
    /create/
    /<int:pk>/edit
    """
    form_class = CarForm
    model = Car
    template = 'car_app/car_form.html'

    def get(self, request, pk=None):
        if pk:  # show update form
            car = get_object_or_404(self.model, pk=pk)
            form = self.form_class(instance=car)
        else:  # show create form
            form = self.form_class()

        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request, pk=None):
        if pk:  # update
            car = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=car)
        else:  # create
            form = self.form_class(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            instance = form.save()
            print(instance.pk)
            return redirect('sbxapp:car-detail', pk=instance.pk)
        else:
            print(form.errors)
            context = {'form': form}
            return render(request, self.template, context)


@require_POST
def car_delete(request, pk):
    """ /<int:pk>/delete/ """
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('sbxapp:car-list')


# --- N+1 problem demo

class PostIndex(generic.ListView):
    # template_name: <app_name>/<model_name>_list.html
    model = Post


class PostIndex2(generic.ListView):
    model = Post
    # eager loading: select_related("One"), prefetch_related("Many")
    queryset = Post.objects.select_related('category').prefetch_related('tags')
