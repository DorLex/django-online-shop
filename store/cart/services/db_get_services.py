from django.shortcuts import get_object_or_404

from cart.models import Carts, CartProducts
from shop.models import Products


def get_user_cart(user):
    """Возвращает корзину пользователя"""
    user_cart = Carts.objects.filter(user=user).only('id').first()  # Если нет, вернет None
    return user_cart


def get_cart_products(user):
    """Возвращает товары, добавленные в корзину пользователя"""

    user_cart = get_user_cart(user)

    cart_products = (
        CartProducts.objects.filter(cart=user_cart)
        .select_related('product', 'cart')
        .only('id', 'product__title', 'product__image', 'quantity',
              'product__price', 'several_price', 'cart__total_price')
    )

    return cart_products


def get_product(product_id):
    """Возвращает один товар"""
    product = get_object_or_404(Products.objects.only('id', 'price'), pk=product_id)
    return product


def get_cart_product_by_product(product, user_cart):
    """Возвращает один товар из корзины"""
    
    cart_product = (
        CartProducts.objects.filter(product=product, cart=user_cart)
        .only('id', 'quantity', 'several_price')
        .first()
    )

    return cart_product


def get_cart_product_by_id(cart_product_id, user_cart):
    """Возвращает один товар из корзины"""
    cart_product = get_object_or_404(CartProducts, pk=cart_product_id, cart=user_cart)
    return cart_product
