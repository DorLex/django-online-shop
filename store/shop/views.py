from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm
from .models import Product, Category


class ShopHome(ListView):
    """Показывает все товары на главной странице"""

    # на результат по умолчанию будет ссылаться context['object_list']
    queryset = Product.objects.all().select_related('category'). \
        only('id', 'slug', 'title', 'image', 'price', 'category__title', )

    context_object_name = 'products'  # добавляем ссылку на context['object_list']
    paginate_by = 3  # пагинация, object_list теперь будет ссылаться на записи одной страницы
    template_name = 'shop/index.html'

    # только dict или list[(key, value),], т.к. используется kwargs.update()
    extra_context = {
        'title': 'Главная страница',
    }

    # прокидываем список всех категорий
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().only('id', 'slug', 'title', )
        context['categories'] = categories

        return context

    # нужен, если контекст формируется с использованием экземпляра данного класса
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # вызываем родительский метод, так как он возвращает paginator и др.
    #     context = super().get_context_data(**kwargs)
    #     # print(self.request.COOKIES.get('sessionid'))
    #     return context

    # добавить куки
    # def render_to_response(self, context, **response_kwargs):
    #     response = super().render_to_response(context, **response_kwargs)
    #     response.set_cookie(key='test', value='my cookie', max_age=2)
    #     return response


class ProductCategory(ListView):
    """Показывает товары выбранной категории"""

    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], ). \
            select_related('category').only('id', 'slug', 'title', 'image', 'price', 'category__title', )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # убрать дубли
        categories = Category.objects.all().only('id', 'slug', 'title', )
        context['categories'] = categories
        category = Category.objects.filter(slug=self.kwargs['category_slug']).values('title')
        context['title'] = category[0]['title']

        return context


class ProductDetail(DetailView):
    """Показывает страницу товара"""

    model = Product
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class RegisterUser(CreateView):
    """Регистрация пользователя"""

    form_class = RegisterUserForm  # используем свою форму
    template_name = 'shop/register.html'
    extra_context = {'title': 'Регистрация', }
    success_url = reverse_lazy('login')  # ленивое перенаправление при успехе


class LoginUser(LoginView):
    """
    Авторизация пользователя;
    при успехе перенаправляет на settings.LOGIN_REDIRECT_URL
    """

    form_class = AuthenticationForm  # используем стандартную форму
    template_name = 'shop/login.html'
    extra_context = {'title': 'Авторизация', }


class LogoutUser(LogoutView):
    """
    Разлогинивает пользователя
    и перенаправляет на settings.LOGOUT_REDIRECT_URL
    """
    pass

#
# def logout_user(request):
#     """Разлогинивает пользователя"""
#     logout(request)
#     return redirect('login')


# class Categories(View):
#     def get(self, request, *args, **kwargs):
#         # kwargs - атрибуты из url (не get)
#
#         response = render(request, 'shop/categories.html')
#         # response.set_cookie(key='test', value='my cookie', max_age=10)
#
#         return response
