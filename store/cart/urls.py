from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartHandler.as_view(), name='cart'),
]
