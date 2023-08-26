from cart.services import db_get_services, calculate_services


def _update_user_cart(user_cart, cart_product):
    """Обновляет корзину пользователя"""
    calculate_services.update_cart_total_price(user_cart, -cart_product.several_price)
    user_cart.save()


def _delete_cart_product(user_cart, cart_product_id):
    """Удаляет товар из корзины"""
    cart_product = db_get_services.get_cart_product_by_id(cart_product_id, user_cart)
    cart_product.delete()
    return cart_product


def delete_from_cart(user, cart_product_id):
    """Удаляет товар из корзины"""
    user_cart = db_get_services.get_user_cart(user)
    cart_product = _delete_cart_product(user_cart, cart_product_id)
    _update_user_cart(user_cart, cart_product)
