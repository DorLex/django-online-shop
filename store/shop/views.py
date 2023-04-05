from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('<h1>Shop main page</h1>')


def categories(request, cat):
    return HttpResponse(f'<h2>{cat}</h2>')
