"""Tests of the show user view."""
from django.test import TestCase
from django.urls import reverse
from translate.models import User, Translation


class ShowUserViewTestCase(TestCase):
    """Tests of the profile view."""

    fixtures = [
        'translate/tests/fixtures/default_user.json',
        'translate/tests/fixtures/other_users.json',
        'translate/tests/fixtures/default_translation.json',
        'translate/tests/fixtures/other_translations.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='MichaelScott')
        self.target_user = User.objects.get(username='DwightSchrute')
        self.url = reverse('profile', kwargs={'pk': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url, f'/profile/{self.user.id}/')

    def test_get_show_user(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse('login') + '?next=' + self.url
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_user_with_valid_id_fails_if_not_self(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('profile', kwargs={'pk': self.target_user.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_get_show_user_with_valid_id_of_self(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "MichaelScott")
        self.assertContains(response, "michaelscott@dundermifflin.com")
        translations = Translation.objects.filter(user_id=self.user.id)
        for translation in translations:
            self.assertContains(response, translation.text_display() + ' -> ' + translation.translated_text_display())

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('profile', kwargs={'pk': self.user.id + 9999})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
