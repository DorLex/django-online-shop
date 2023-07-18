from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm
from .models import Products
from .utils import DataMixin


class ShopHome(DataMixin, ListView):
    """Показывает все товары на главной странице"""

    # на результат по умолчанию будет ссылаться context['object_list']
    def get_queryset(self):
        products = Products.objects.all() \
            .select_related('category') \
            .prefetch_related(
            Prefetch(
                'users_favorites',
                queryset=User.objects.filter(pk=self.request.user.pk).only('id', ),
                to_attr='in_user_favorites'
            )
        ).only('id', 'slug', 'title', 'image', 'price', 'category__title', )

        return products

    context_object_name = 'products'  # добавляем ссылку на context['object_list']
    template_name = 'shop/index.html'

    # нужен, если контекст формируется с использованием экземпляра данного класса
    def get_context_data(self, *, object_list=None, **kwargs):
        # вызываем родительский метод, так как он возвращает paginator и др.
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        context['title'] = 'Главная страница'

        return context

    # добавить куки
    # def render_to_response(self, context, **response_kwargs):
    #     response = super().render_to_response(context, **response_kwargs)
    #     response.set_cookie(key='test', value='my cookie', max_age=2)
    #     return response


class ProductsCategory(DataMixin, ListView):
    """Показывает товары выбранной категории"""

    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Products.objects.filter(category__slug=self.kwargs['category_slug'], ) \
            .select_related('category') \
            .only('id', 'slug', 'title', 'image', 'price', 'category__title', )
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        context['category_selected'] = self.kwargs['category_slug']

        return context


class ProductDetail(DetailView):
    """Показывает страницу товара"""

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


class ShowFavorites(ListView):
    template_name = 'shop/favorites.html'
    context_object_name = 'favorites_products'
    paginate_by = 3

    def get_queryset(self):
        favorites_products = Products.objects.filter(users_favorites=self.request.user) \
            .select_related('category') \
            .only('id', 'slug', 'title', 'image', 'price', 'category__title', )
        return favorites_products

# class ShowFavorites(View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#
#         favorites_products = Products.objects.filter(users_favorites=user).only('title')
#
#         return render(request, 'shop/favorites.html', context={'test': favorites_products})
