from django.shortcuts import render, redirect
from django.views import View

from .models import Cart, CartProduct


class CartView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_cart = Cart.objects.filter(user=user).first()  # мб сделать как в Add???
        if not user_cart:
            return render(request, 'cart/cart.html', )

        cart_products = CartProduct.objects.filter(cart=user_cart).select_related('product'). \
            only('product__title', 'quantity', 'product__price', )

        return render(request, 'cart/cart.html', context={'cart_products': cart_products, })


class CartAdd(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = kwargs.get('product_id')

        user_cart = Cart.objects.filter(user=user).first()
        if not user_cart:
            user_cart = Cart.objects.create(user=user)

        cart_product = CartProduct.objects.create(product_id=product_id, quantity=2, cart=user_cart)

        # user_cart = Cart.objects.filter(user=user).values('id')  # возвращает <QuerySet [{'id': 6}]>
        # if len(user_cart) == 0:  # тут выполняется user_cart запрос
        #     user_cart = Cart.objects.create(user=user)
        # cart_product = CartProduct.objects.create(product_id=product_id, quantity=2, cart_id=user_cart[0].get('id'))

        return redirect('cart_view')
