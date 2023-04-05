from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('categories/<slug:cat>/', views.categories),
    
]
