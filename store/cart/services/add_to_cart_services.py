from cart.models import Carts, CartProducts
from cart.services import db_get_services, calculate_services


def _create_user_cart(user, several_price):
    """Создает корзину пользователя"""
    user_cart = Carts.objects.create(user=user, total_price=several_price)
    return user_cart


def _create_cart_product(product, product_quantity, several_price, user_cart):
    """Создает товар в корзине"""
    cart_product = CartProducts.objects.create(product=product, quantity=product_quantity,
                                               several_price=several_price, cart=user_cart)
    return cart_product


def _update_total_price_user_cart(user_cart, added_value):
    """Обновляет общую стоимость корзины"""
    calculate_services.increase_cart_total_price(user_cart, added_value)
    user_cart.save()


def _update_cart_product(cart_product, product_quantity, several_price, user_cart):
    """Обновляет товар в корзине"""
    calculate_services.increase_cart_product_quantity(cart_product, product_quantity)
    calculate_services.increase_cart_product_several_price(cart_product, several_price)
    cart_product.save()


def _update_user_cart(product, product_quantity, several_price, user_cart):
    """Обновляет корзину пользователя"""

    cart_product = db_get_services.get_one_cart_product(product, user_cart)

    if cart_product:
        _update_cart_product(cart_product, product_quantity, several_price, user_cart)
    else:
        _create_cart_product(product, product_quantity, several_price, user_cart)

    _update_total_price_user_cart(user_cart, several_price)


def add_to_cart(user, product_id, product_quantity):
    """Добавляет товар в корзину"""
    
    product = db_get_services.get_product(product_id)
    several_price = calculate_services.calculate_several_price(product, product_quantity)

    user_cart = db_get_services.get_user_cart(user)
    if user_cart:
        _update_user_cart(product, product_quantity, several_price, user_cart)
    else:
        user_cart = _create_user_cart(user, several_price)
        _create_cart_product(product, product_quantity, several_price, user_cart)
