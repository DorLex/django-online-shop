from django.shortcuts import render, redirect
from django.views import View

from .models import Cart, CartProduct


class CartView(View):
    """Отображение корзины"""

    def get(self, request, *args, **kwargs):
        user = request.user
        user_cart = Cart.objects.filter(user=user).first()
        if not user_cart:
            return render(request, 'cart/cart.html', context={'title': 'Корзина', })

        cart_products = CartProduct.objects.filter(cart=user_cart).select_related('product'). \
            only('id', 'product__title', 'product__image', 'quantity', 'product__price', )

        for cart_product in cart_products:
            cart_product.several_price = cart_product.quantity * cart_product.product.price

        total_price = sum(cart_product.several_price for cart_product in cart_products)

        return render(request, 'cart/cart.html',
                      context={'title': 'Корзина', 'cart_products': cart_products, 'total_price': total_price})


class CartAdd(View):
    """Добавление товара в корзину"""

    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        product_quantity = request.POST.get('product_quantity')

        user_cart = Cart.objects.filter(user=user).first()
        if user_cart:
            product_in_cart = CartProduct.objects.filter(product_id=product_id, cart=user_cart).first()
            if product_in_cart:
                product_in_cart.quantity += int(product_quantity)
                product_in_cart.save()
            else:
                CartProduct.objects.create(product_id=product_id, quantity=product_quantity, cart=user_cart)
        else:
            user_cart = Cart.objects.create(user=user)
            CartProduct.objects.create(product_id=product_id, quantity=product_quantity, cart=user_cart)

        return redirect('cart_view')


class CartDelete(View):
    """Убирает товар из корзины"""

    def post(self, request, cart_product_id, *args, **kwargs):
        user_cart = Cart.objects.get(user=request.user)
        product_in_cart = CartProduct.objects.get(pk=cart_product_id, cart=user_cart)
        product_in_cart.delete()

        return redirect('cart_view')
