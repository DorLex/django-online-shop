from django.contrib import admin
from django.utils.html import format_html

from . import models


class ProductAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы Product в админке"""

    # список отображаемых полей
    list_display = (
        'id', 'title', 'get_html_image', 'price', 'quantity', 'time_created', 'time_updated', 'category',
    )
    list_display_links = ('id', 'title',)  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('title', 'description',)  # поля, по которым можно будет производить поиск записей
    list_filter = ('category', 'time_created', 'time_updated',)  # поля, по которым можем фильтровать список товаров
    prepopulated_fields = {'slug': ('title',)}  # автоматически заполняет поле slug по данным поля title

    # возвращает html тег с изображением
    def get_html_image(self, product):
        if product.image:
            print(product.image.url)
            return format_html('<img src="{}" height=50>', product.image.url)
        else:
            return 'Нет изображения'

    # переименует поле в админке
    get_html_image.short_description = 'Изображение'


class CategoryAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы Category в админке"""

    list_display = ('id', 'title',)  # список отображаемых полей
    list_display_links = ('id', 'title',)  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('title',)  # поля, по которым можно будет производить поиск записей
    prepopulated_fields = {'slug': ('title',)}  # автоматически заполняет поле slug по данным поля title


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
