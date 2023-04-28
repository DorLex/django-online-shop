from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShopHome.as_view(), name='home'),
    # path('categories/<slug:category>/', views.categories, name='categories'),
    path('categories/<slug:category>/', views.Categories.as_view(), name='categories'),
]
