from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# from .models import Product


class ShopHome(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Main Page',
        }
        return render(request, 'shop/index.html', context=context)


# def index(request):
#     context = {
#         'title': 'Main Page',
#     }
#     return render(request, 'shop/index.html', context=context)


# class ShopHome(ListView):
#     model = Product
#     template_name = 'shop/index.html'
#
#     # extra_context = {'title': {'one': 2}, }
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Main Page'
#
#         return context


# def categories(request, category):
#     return HttpResponse(f'<h2>{category}</h2>')


class Categories(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse(f'<h2>{args}, {kwargs}</h2>')
        return render(request, 'shop/categories.html', context=kwargs)
