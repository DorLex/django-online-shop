from .models import Categories


def show_categories(request):
    """Прокидываем список всех категорий"""
    categories = Categories.objects.all().only('id', 'slug', 'title', )
    context = {'categories': categories, }
    return context
