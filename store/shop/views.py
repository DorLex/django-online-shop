from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm
from .models import Products
from .utils import DataMixin


class ShopHome(DataMixin, ListView):
    """Отображает все товары на главной странице"""

    extra_context = {'title': 'Главная страница', }

    # на результат по умолчанию будет ссылаться context['object_list']
    def get_queryset(self):
        products = Products.objects.all() \
            .select_related('category') \
            .prefetch_related(
            Prefetch(
                'users_favorites',
                queryset=User.objects.filter(pk=self.request.user.pk).only('id', ),  # фильтруем связанную таблицу М2М
                to_attr='in_user_favorites'  # атрибут будет доступен у каждого элемента products
            )
        ).only('id', 'slug', 'title', 'image', 'price', 'category__title', )

        return products

    context_object_name = 'products'  # добавляем ссылку на context['object_list']
    template_name = 'shop/index.html'

    # нужен, если контекст формируется с использованием экземпляра данного класса
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # вызываем родительский метод, так как он возвращает paginator и др.
    #     context = super().get_context_data(**kwargs)
    #     # context.update(self.get_common_context())
    #     context['title'] = 'Главная страница'
    #
    #     return context

    # добавить куки
    # def render_to_response(self, context, **response_kwargs):
    #     response = super().render_to_response(context, **response_kwargs)
    #     response.set_cookie(key='test', value='my cookie', max_age=2)
    #     return response


class ProductsCategory(DataMixin, ListView):
    """Отображает товары выбранной категории"""

    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Products.objects.filter(category__slug=self.kwargs['category_slug'], ) \
            .select_related('category') \
            .prefetch_related(
            Prefetch(
                'users_favorites',
                queryset=User.objects.filter(pk=self.request.user.pk).only('id', ),
                to_attr='in_user_favorites'
            )
        ).only('id', 'slug', 'title', 'image', 'price', 'category__title', )

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = self.kwargs['category_slug']

        return context


class ShowFavorites(DataMixin, ListView):
    """Отображает список избранного"""

    template_name = 'shop/favorites.html'
    context_object_name = 'favorites_products'
    extra_context = {'title': 'Избранное', }

    def get_queryset(self):
        favorites_products = Products.objects.filter(users_favorites=self.request.user) \
            .select_related('category') \
            .only('id', 'slug', 'title', 'image', 'price', 'category__title', )
        return favorites_products


class AddToFavorites(View):
    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        product = Products.objects.get(pk=product_id)
        user.favorites_products.add(product)

        return redirect('home')


class RemoveFromFavorites(View):
    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        product = Products.objects.get(pk=product_id)
        user.favorites_products.remove(product)

        return redirect('home')


class ProductDetail(DetailView):
    """Отображает страницу товара"""

    model = Products
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class RegisterUser(CreateView):
    """Регистрация пользователя"""

    form_class = RegisterUserForm  # используем свою форму
    template_name = 'shop/register.html'
    extra_context = {'title': 'Регистрация', }  # только dict или list[(key, value),], т.к. используется kwargs.update()
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


class PageNotFound(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/error_404.html')

# class ShowFavorites(View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#
#         favorites_products = Products.objects.filter(users_favorites=user).only('title')
#
#         return render(request, 'shop/favorites.html', context={'test': favorites_products})
