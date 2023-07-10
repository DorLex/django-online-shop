from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from shop.models import Product
from .models import Cart, CartProduct


class CartView(ListView):
    template_name = 'cart/cart.html'
    paginate_by = 5
    context_object_name = 'cart_products'

    def get_queryset(self):
        user = self.request.user
        user_cart = Cart.objects.filter(user=user).only('id').first()
        cart_products = CartProduct.objects.filter(cart=user_cart).select_related('product', 'cart'). \
            only('id', 'product__title', 'product__image', 'quantity', 'product__price',
                 'several_price', 'cart__total_price')

        return cart_products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'

        return context


class CartAdd(View):
    """Добавление товара в корзину"""

    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        product = Product.objects.get(pk=product_id)
        product_quantity = request.POST.get('product_quantity')
        several_price = product.price * int(product_quantity)

        user_cart = Cart.objects.filter(user=user).first()
        if user_cart:
            product_in_cart = CartProduct.objects.filter(product=product, cart=user_cart).first()
            if product_in_cart:
                product_in_cart.quantity += int(product_quantity)
                product_in_cart.several_price += several_price
                product_in_cart.save()
                user_cart.total_price += several_price
                user_cart.save()
            else:
                product_in_cart = CartProduct.objects.create(
                    product=product,
                    quantity=product_quantity,
                    several_price=several_price,
                    cart=user_cart
                )
                user_cart.total_price += several_price
                user_cart.save()
        else:
            user_cart = Cart.objects.create(user=user, total_price=several_price)
            CartProduct.objects.create(product=product, quantity=product_quantity,
                                       several_price=several_price, cart=user_cart)

        return redirect('cart_view')


class CartDelete(View):
    """Убирает товар из корзины"""

    def post(self, request, cart_product_id, *args, **kwargs):
        user_cart = Cart.objects.get(user=request.user)
        product_in_cart = CartProduct.objects.get(pk=cart_product_id, cart=user_cart)
        product_in_cart.delete()
        user_cart.total_price -= product_in_cart.several_price
        user_cart.save()

        return redirect('cart_view')
