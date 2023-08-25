from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestRegistrationAuthentication(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = {
            'username': 'test_username_1',
            'email': 'test_email@example.com',
            'password1': 'test1test1test1',
            'password2': 'test1test1test1',
        }

    def registration(self):
        url_registration = reverse('register')
        response_registration = self.client.post(url_registration, data=self.user)
        return response_registration

    def test_registration(self):
        self.registration()

        users = User.objects.all()
        self.assertEqual(1, users.count())

    def test_authentication(self):
        self.registration()

        url_login = reverse('login')
        response_login = self.client.post(url_login, data={
            'username': 'test_username_1',
            'password': 'test1test1test1',
        })

        self.assertEqual(302, response_login.status_code)

        url_home = reverse('home')
        response_home = self.client.get(url_home)
        user = response_home.context.get('user')

        self.assertTrue(user.is_authenticated)
