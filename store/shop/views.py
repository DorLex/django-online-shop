from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('<h1>Shop main page</h1>')


def categories(request, category):
    return HttpResponse(f'<h2>{category}</h2>')
