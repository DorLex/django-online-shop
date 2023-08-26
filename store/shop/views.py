from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm
from .models import Products
from .services import db_services
from .utils import DataMixin


class ShopHome(DataMixin, ListView):
    """Отображает все товары на главной странице"""

    extra_context = {'title': 'Главная страница', }  # dict или list[(key, value),], т.к. используется kwargs.update()
    context_object_name = 'products'  # добавляем ссылку на context['object_list']
    template_name = 'shop/index.html'

    # на результат по умолчанию будет ссылаться context['object_list']
    def get_queryset(self):
        products = db_services.get_all_products(self.request.user)
        return products

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
        products = db_services.get_products_of_selected_category(
            self.kwargs['category_slug'], self.request.user
        )
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = self.kwargs['category_slug']

        return context


class ShowFavorites(DataMixin, ListView):
    """Отображает товары, добавленные в избранное"""

    template_name = 'shop/favorites.html'
    context_object_name = 'favorites_products'
    extra_context = {'title': 'Избранное', }

    def get_queryset(self):
        favorites_products = db_services.get_favorites_products(self.request.user)
        return favorites_products


class AddToFavorites(View):
    """Добавляет товар в избранное"""

    def post(self, request, product_id, *args, **kwargs):
        db_services.add_to_favorites(request.user, product_id)
        return redirect('home')


class RemoveFromFavorites(View):
    """Убирает товар их избранного"""

    def post(self, request, product_id, *args, **kwargs):
        db_services.remove_from_favorites(request.user, product_id)
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


class PageNotFound(View):
    """Отображает страницу с кодом 404"""

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/error_404.html')
