from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Categories, Products


class TestCartViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test2', password='test2test2test2')

        cls.category_2 = Categories.objects.create(
            title='тестовая категория 2',
            slug='test-category-2',
        )

        cls.product_2 = Products.objects.create(
            title='Тестовый товар 2',
            slug='test-product-2',
            image='test-image',
            description='Описание тестового товара 2',
            price=15000,
            quantity=3,
            category=cls.category_2,
        )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_cart_view(self):
        url = reverse('cart_view')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_add_to_cart(self):
        url_to_add = reverse('cart_add', args=[self.product_2.id], )
        response_to_add = self.client.post(url_to_add, data={'product_quantity': '2'})
        self.assertEqual(302, response_to_add.status_code)

        url_get = reverse('cart_view')
        response_get = self.client.get(url_get)
        self.assertIn('Тестовый товар 2', response_get.content.decode())
