from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestShopView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test1', password='test1test1test1')

    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_categories(self):
        url = reverse('product_category', args=['tv'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_favorites(self):
        self.client.force_login(user=self.user)
        url = reverse('favorites_products')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
