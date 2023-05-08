from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации"""

    class Meta:
        model = User  # в какую модель сохраняет
        fields = ('username', 'email', 'password1', 'password2')  # список отображаемых полей
