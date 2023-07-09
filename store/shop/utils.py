from .models import Category


class DataMixin:
    """Общий контекст для ListView"""

    paginate_by = 3  # пагинация, context_object_name теперь будет ссылаться на записи одной страницы

    def get_common_context(self):
        # прокидываем список всех категорий
        categories = Category.objects.all().only('id', 'slug', 'title', )
        context = {'categories': categories, }
        return context
