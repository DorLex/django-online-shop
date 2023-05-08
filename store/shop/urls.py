from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.ShopHome.as_view(), name='home'),
                  path('register/', views.RegisterUser.as_view(), name='register'),
                  path('login/', views.LoginUser.as_view(), name='login'),
                  path('logout/', views.LogoutUser.as_view(), name='logout'),
                  path('categories/<slug:category>/', views.Categories.as_view(), name='categories'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для изображений
