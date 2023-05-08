from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm
from .models import Product


class ShopHome(ListView):
    """Показывает все товары"""
    model = Product
    # на результат будет ссылаться context['object_list']
    queryset = model.objects.all().select_related('category'). \
        only('title', 'image', 'description', 'price', 'category__title', )
    context_object_name = 'products'  # добавляем ссылку на context['object_list']
    paginate_by = 2  # пагинация, object_list теперь будет ссылаться на записи одной страницы
    template_name = 'shop/index.html'
    extra_context = {
        'title': 'Главная страница',
    }  # только dict или list[(key, value),], т.к. используется kwargs.update()

    # нужен, если контекст формируется с использованием экземпляра данного класса
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # вызываем родительский метод, так как он возвращает paginator и др.
    #     context = super().get_context_data(**kwargs)
    #     return context


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
    Разлогинит пользователя
    и перенаправляет на settings.LOGOUT_REDIRECT_URL
    """
    pass


# def logout_user(request):
#     """Разлогинит пользователя"""
#     logout(request)
#     return redirect('login')


class Categories(View):
    def get(self, request, *args, **kwargs):
        # kwargs - атрибуты из url (не get)

        return render(request, 'shop/categories.html')
