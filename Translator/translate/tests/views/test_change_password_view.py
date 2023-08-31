"""Tests of the change password view."""
from django.test import TestCase
from django.urls import reverse

from translate.models import User


class HomeViewTestCase(TestCase):
    """Tests of the change password view."""

    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('password_change')
        self.user = User.objects.get(username='MichaelScott')
        self.form = {"old_password": "Password123", "new_password1": "ThisIsMyPassword",
                     "new_password2": "ThisIsMyPassword"}

    def test_change_password_url(self):
        self.assertEqual(self.url, '/password_change/')

    def test_get_change_password(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')

    def test_post_change_password(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_post_change_password_with_wrong_old_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form['old_password'] = 'WrongPassword'
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')

    def test_post_change_password_with_blank_old_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form['old_password'] = ''
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')

    def test_post_change_password_with_blank_new_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form['new_password1'] = ''
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')

    def test_post_change_password_with_blank_confirm_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form['new_password2'] = ''
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')

    def test_post_change_password_with_mismatched_passwords(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form['new_password2'] = 'ThatIsNotMyPassword'
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')
