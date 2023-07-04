from django.shortcuts import render
from django.views import View

from .models import Cart, CartProduct


class CartHandler(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_cart = Cart.objects.filter(user=user).first()
        if not user_cart:
            user_cart = Cart.objects.create(user=user)

        cart_products = CartProduct.objects.filter(cart=user_cart).select_related('product'). \
            only('product__title', 'quantity', 'product__price', )

        return render(request, 'cart/cart.html', context={'cart_products': cart_products, })

    def post(self):
        user_cart = Cart.objects.all()
