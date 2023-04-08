from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        'title': 'Main Page',
    }
    return render(request, 'shop/index.html', context=context)


def categories(request, category):
    return HttpResponse(f'<h2>{category}</h2>')
