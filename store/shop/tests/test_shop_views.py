from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from shop.models import Products, Categories


class TestShopView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test1', password='test1test1test1')

        cls.category_1 = Categories.objects.create(
            title='тестовая категория 1',
            slug='test-category-1',
        )

        cls.product_1 = Products.objects.create(
            title='Тестовый товар 1',
            slug='test-product-1',
            image='test-image',
            description='Описание тестового товара 1',
            price=15000,
            quantity=3,
            category=cls.category_1,
        )

    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIn('Тестовый товар 1', response.content.decode())

    def test_categories(self):
        url = reverse('product_category', args=['test-category-1'])
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIn('Тестовый товар 1', response.content.decode())
        self.assertIn('тестовая категория 1', response.content.decode())

    def test_add_to_favorites(self):
        self.client.force_login(user=self.user)

        url_to_add = reverse('add_to_favorites', args=[self.product_1.id])
        response_to_add = self.client.post(url_to_add)
        self.assertEqual(302, response_to_add.status_code)

        url_get = reverse('favorites_products')
        response_get = self.client.get(url_get)
        self.assertIn('Тестовый товар 1', response_get.content.decode())
