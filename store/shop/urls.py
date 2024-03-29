from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShopHome.as_view(), name='home'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('products/<slug:product_slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('categories/<slug:category_slug>/', views.ProductsCategory.as_view(), name='product_category'),
    path('favorites/', views.ShowFavorites.as_view(), name='favorites_products'),
    path('remove_from_favorites/<int:product_id>/', views.RemoveFromFavorites.as_view(), name='remove_from_favorites'),
    path('add_to_favorites/<int:product_id>/', views.AddToFavorites.as_view(), name='add_to_favorites'),
]
