from django.core.cache import cache

from .models import Categories


def show_categories(request):
    """Добавляет в контекст список всех категорий"""

    categories = cache.get('categories')

    if not categories:
        categories = Categories.objects.all().only('id', 'slug', 'title', )
        cache.set('categories', categories, 60)

    context = {'categories': categories, }

    return context
