from django.shortcuts import render, redirect


def top(request):
    return render(request, 'top.html')
