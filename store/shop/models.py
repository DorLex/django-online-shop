from django.contrib.auth.models import User
from django.db import models


class Products(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='products_images/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    category = models.ForeignKey('Categories', related_name='products',
                                 on_delete=models.PROTECT, verbose_name="Категория")

    users_favorites = models.ManyToManyField(User, blank=True, related_name='favorites_products',
                                             verbose_name='Избранное пользователей')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
