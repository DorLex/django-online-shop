from django.db.models import F


def calculate_several_price(product, product_quantity):
    """Считает стоимость нескольких одинаковых товаров"""
    several_price = product.price * int(product_quantity)
    return several_price


def increase_cart_product_quantity(cart_product, product_quantity):
    """Прибавляет количество одинаковых товаров в корзине"""
    cart_product.quantity = F('quantity') + int(product_quantity)


def increase_cart_product_several_price(cart_product, several_price):
    """Прибавляет стоимость одинаковых товаров в корзине"""
    cart_product.several_price = F('several_price') + int(several_price)


def update_cart_total_price(user_cart, value):
    """Обновляет общую стоимость корзины"""
    user_cart.total_price = F('total_price') + int(value)
