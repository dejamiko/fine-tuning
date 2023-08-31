from django.test import TestCase
from django.urls import reverse

from translate.models import User
from translate.tests.helpers import LogInTester

"""Tests of the log in view. The structure of the tests was inspired by the Clucker project from 5CCS2SEG."""


class LogInViewTest(TestCase, LogInTester):
    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.get(username='MichaelScott')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/login/')

    def test_unsuccessful_log_in(self):
        form_input = {'username': 'MichaelScott', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {'username': 'MichaelScott', 'password': 'Password123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, reverse('home'))

    def test_successful_log_in_with_redirect(self):
        redirect_url = reverse('profile', kwargs={'pk': self.user.id})
        form_input = {'username': 'MichaelScott', 'password': 'Password123', 'next': redirect_url}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_get_log_in_with_redirect(self):
        redirect_url = reverse('profile', kwargs={'pk': self.user.id})
        self.url = reverse('login') + '?next=' + redirect_url
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEqual(response.context['next'], redirect_url)

    def test_get_log_in_redirects_to_home_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_log_in_redirects_to_home_when_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        form_input = {'username': 'wronguser', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
