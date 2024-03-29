from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from .services import add_to_cart_services, delete_from_cart_services, db_get_services


class CartView(ListView):
    """Отображает товары, добавленные в корзину пользователя"""

    template_name = 'cart/cart.html'
    paginate_by = 3
    context_object_name = 'cart_products'
    extra_context = {'title': 'Корзина'}

    def get_queryset(self):
        cart_products = db_get_services.get_cart_products(self.request.user)
        return cart_products


class CartAdd(View):
    """Добавление товара в корзину"""

    def post(self, request, product_id, *args, **kwargs):
        product_quantity = request.POST.get('product_quantity')
        add_to_cart_services.add_to_cart(request.user, product_id, product_quantity)

        return redirect('cart_view')


class CartDelete(View):
    """Убирает товар из корзины"""

    def post(self, request, cart_product_id, *args, **kwargs):
        delete_from_cart_services.delete_from_cart(request.user, cart_product_id)
        return redirect('cart_view')
