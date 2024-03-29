from django.contrib import admin

from . import models


class CartAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы Cart в админке"""

    # список отображаемых полей
    list_display = (
        'id',
        'user',
        'total_price',
        'time_created',
        'time_updated',
    )

    list_display_links = ('id', 'user',)  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('user__username',)  # поля, по которым можно будет производить поиск записей
    list_filter = ('time_created', 'time_updated')  # поля, по которым можем фильтровать список


class CartProductAdmin(admin.ModelAdmin):
    """Настраивает отображение таблицы CartProduct в админке"""

    # список отображаемых полей
    list_display = (
        'id',
        'product',
        'quantity',
        'several_price',
        'time_created',
        'time_updated',
        'cart',
    )

    list_display_links = ('id', 'product')  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('product__title',)  # поля, по которым можно будет производить поиск записей
    list_filter = ('cart', 'time_created', 'time_updated')  # поля, по которым можем фильтровать список


admin.site.register(models.Carts, CartAdmin)
admin.site.register(models.CartProducts, CartProductAdmin)
