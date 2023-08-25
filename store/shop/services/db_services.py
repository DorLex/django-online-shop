from django.contrib.auth.models import User
from django.db.models import Prefetch

from shop.models import Products


def get_all_products(user):
    """Возвращает список всех товаров из db"""

    products = Products.objects.all() \
        .select_related('category') \
        .prefetch_related(
        Prefetch(
            'users_favorites',
            queryset=User.objects.filter(pk=user.pk).only('id', ),  # фильтруем связанную таблицу М2М
            to_attr='in_user_favorites'  # атрибут будет доступен у каждого элемента products
        )
    ).only('id', 'slug', 'title', 'image', 'price', 'category__title', )

    return products


def get_products_of_selected_category(category_slug, user):
    """Возвращает товары выбранной категории"""

    products = Products.objects.filter(category__slug=category_slug) \
        .select_related('category') \
        .prefetch_related(
        Prefetch(
            'users_favorites',
            queryset=User.objects.filter(pk=user.pk).only('id', ),
            to_attr='in_user_favorites'
        )
    ).only('id', 'slug', 'title', 'image', 'price', 'category__title', )

    return products
