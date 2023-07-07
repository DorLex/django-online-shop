from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShopHome.as_view(), name='home'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('product/<slug:product_slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('categories/<slug:category_slug>/', views.ProductsCategory.as_view(), name='products_category'),
]
