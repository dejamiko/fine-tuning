"""Tests of the log out view."""
from django.test import TestCase
from django.urls import reverse
from translate.models import User
from translate.tests.helpers import LogInTester


class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the logout view."""

    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('logout')
        self.user = User.objects.get(username='MichaelScott')

    def test_log_out_url(self):
        self.assertEqual(self.url, '/logout/')

    def test_get_log_out(self):
        self.client.login(username='MichaelScott', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())

    def test_log_out_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(self._is_logged_in())
