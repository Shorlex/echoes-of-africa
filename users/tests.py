from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.

class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login(self):
        login = self.client.login(username='testuser', password='password')
        self.assertTrue(login)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)  # Redirect after logout


class UserAuthorizationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_unauthorized_user_redirect(self):
        response = self.client.get(reverse('post_hero'))
        self.assertEqual(response.status_code, 302)  # Redirect if not logged in

    def test_authorized_user_can_create_hero(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('post_hero'))
        self.assertEqual(response.status_code, 200)  # Authorized users can access

    def test_unauthorized_user_cannot_create_hero(self):
        response = self.client.get(reverse('post_hero'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, '/users/login/?next=/heroes/post_hero/')

    def test_user_login(self):
        response = self.client.post('/users/login/', {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        self.assertRedirects(response, '/heroes/')

    def test_user_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertRedirects(response, '/')