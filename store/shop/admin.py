from django.contrib import admin

from . import models


class ProductAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы Product в админке"""

    list_display = (
        'id', 'title', 'image', 'price', 'quantity', 'time_created', 'time_updated',
    )  # список отображаемых полей
    
    list_display_links = ('id', 'title')  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('title', 'description')  # поля, по которым можно будет производить поиск записей
    list_filter = ('time_created', 'time_updated',)  # поля, по которым можем фильтровать список товаров
    prepopulated_fields = {'slug': ('title',)}  # автоматически заполняет поле slug по данным поля title


class CategoryAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы Category в админке"""

    list_display = ('id', 'title',)  # список отображаемых полей
    list_display_links = ('id', 'title')  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('title',)  # поля, по которым можно будет производить поиск записей
    prepopulated_fields = {'slug': ('title',)}  # автоматически заполняет поле slug по данным поля title


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
