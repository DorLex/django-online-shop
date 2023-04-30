from django.shortcuts import render
from django.views import View

from .models import Product, Category


class ShopHome(View):
    def get(self, request, *args, **kwargs):
        phones = Product.objects.select_related('category').filter(category__title='phones')

        context = {'title': 'Main Page', 'phones': phones, }
        return render(request, 'shop/index.html', context=context)

    def post(self, request, *args, **kwargs):
        context = {'test': request.POST, }
        return render(request, 'shop/index.html', context=context)


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


class Categories(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/categories.html', context=kwargs)
