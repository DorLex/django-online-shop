from .models import Categories


class DataMixin:
    """Общий контекст для ListView"""

    paginate_by = 3  # пагинация, context_object_name теперь будет ссылаться на записи одной страницы

    # def get_common_context(self):
    #     return context
