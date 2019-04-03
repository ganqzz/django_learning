from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PizzaForm, MultiplePizzaForm
from .models import Pizza


def home(request):
    return render(request, 'pizza/home.html')


def list_order(request):
    orders = Pizza.objects.all()
    return render(request, 'pizza/list.html', {'orders': orders})


# create
def order(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request,
                             'Thanks for ordering! Your {} {} and {} pizza is on its way!'.format(
                                 instance.get_size_display(),
                                 instance.topping1,
                                 instance.topping2,
                             ))
            return redirect('pizza:detail', pk=instance.pk)
        else:
            messages.warning(request, 'Not ordered, please try again.')
            multiple_form = MultiplePizzaForm()
            return render(request, 'pizza/order.html',
                          {'multiple_form': multiple_form, 'pizzaform': form})

    # GET
    multiple_form = MultiplePizzaForm()
    form = PizzaForm()
    return render(request, 'pizza/order.html',
                  {'multiple_form': multiple_form, 'pizzaform': form})


# detail & edit
def detail(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == 'POST':
        form = PizzaForm(request.POST, instance=pizza)
        if form.is_valid():
            instance = form.save()
            messages.success(request, 'Your order has been updated successfully.')
            return redirect('pizza:detail', pk=instance.pk)
        else:
            messages.warning(request, 'Your order has not been updated.')
            return render(request, 'pizza/order_detail.html', {'pizzaform': form})

    # GET detail
    form = PizzaForm(instance=pizza)
    return render(request, 'pizza/order_detail.html', {'pizzaform': form})


# formset demo
def order_pizzas(request):
    if request.method == 'POST':
        PizzaFormSet = formset_factory(PizzaForm)
        formset = PizzaFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                print(instance)
                # instance.save()  # 省略
            messages.success(request, 'Pizzas have been ordered!')
            return redirect('pizza:list')
        else:
            messages.warning(request, 'Not ordered.')
            return render(request, 'pizza/order_pizzas.html', {'formset': formset})

    # GET
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    else:
        number_of_pizzas = 2

    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    return render(request, 'pizza/order_pizzas.html', {'formset': formset})


# delete
def delete(request, pk):
    if request.method == 'POST':
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.delete()
        messages.success(request, 'Deleted.')
    return redirect('pizza:list')
