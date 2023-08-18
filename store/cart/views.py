from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from shop.models import Products
from .models import Carts, CartProducts


class CartView(ListView):
    template_name = 'cart/cart.html'
    paginate_by = 3
    context_object_name = 'cart_products'
    extra_context = {'title': 'Корзина'}

    def get_queryset(self):
        user = self.request.user
        user_cart = Carts.objects.filter(user=user).only('id').first()
        cart_products = CartProducts.objects.filter(cart=user_cart) \
            .select_related('product', 'cart') \
            .only('id', 'product__title', 'product__image', 'quantity', 'product__price',
                  'several_price', 'cart__total_price')

        return cart_products


class CartAdd(View):
    """Добавление товара в корзину"""

    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        product = Products.objects.filter(pk=product_id).only('id', 'price').first()
        product_quantity = request.POST.get('product_quantity')
        several_price = product.price * int(product_quantity)

        user_cart = Carts.objects.filter(user=user).only('id', 'total_price').first()
        if user_cart:
            cart_product = CartProducts.objects.filter(product=product, cart=user_cart). \
                only('id', 'quantity', 'several_price').first()
            if cart_product:
                cart_product.quantity += int(product_quantity)
                cart_product.several_price += several_price
                cart_product.save()
                user_cart.total_price += several_price
                user_cart.save()
            else:
                CartProducts.objects.create(product=product, quantity=product_quantity,
                                            several_price=several_price, cart=user_cart)
                user_cart.total_price += several_price
                user_cart.save()
        else:
            user_cart = Carts.objects.create(user=user, total_price=several_price)
            CartProducts.objects.create(product=product, quantity=product_quantity,
                                        several_price=several_price, cart=user_cart)

        return redirect('cart_view')


class CartDelete(View):
    """Убирает товар из корзины"""

    def post(self, request, cart_product_id, *args, **kwargs):
        user_cart = Carts.objects.get(user=request.user)
        product_in_cart = CartProducts.objects.get(pk=cart_product_id, cart=user_cart)
        product_in_cart.delete()
        user_cart.total_price -= product_in_cart.several_price
        user_cart.save()

        return redirect('cart_view')
