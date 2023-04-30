from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.ShopHome.as_view(), name='home'),
                  path('categories/<slug:category>/', views.Categories.as_view(), name='categories'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для картинок
