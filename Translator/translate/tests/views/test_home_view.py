"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse

from translate.models import User, Translation


class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['translate/tests/fixtures/default_user.json', 'translate/tests/fixtures/default_translation.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='MichaelScott')
        self.form = {'text': 'Hello world!', 'language': 'English'}

    def test_home_url(self):
        self.assertEqual(self.url, '/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_home_with_translation(self):
        response = self.client.get(self.url, {'translation': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Hello world!', response.content.decode('utf-8'))

    def test_post_home(self):
        count_before = Translation.objects.count()
        response = self.client.post(self.url, self.form)
        count_after = Translation.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Hello world!', response.content.decode('utf-8'))
        self.assertInHTML('Witaj świecie! Witaj świecie!', response.content.decode('utf-8'))
        self.assertEqual(count_after, count_before + 1)
        translation = Translation.objects.last()
        self.assertEqual(translation.text, 'Hello world!')
        self.assertEqual(translation.translated_text, 'Witaj świecie! Witaj świecie!')
        self.assertEqual(translation.user, None)

    def test_post_home_with_an_existing_translation(self):
        self.client.login(username=self.user.username, password='Password123')
        count_before = Translation.objects.count()
        response = self.client.post(self.url, self.form)
        count_after = Translation.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Hello world!', response.content.decode('utf-8'))
        self.assertInHTML('Witaj świecie! Witaj świecie!', response.content.decode('utf-8'))
        self.assertEqual(count_after, count_before)
        translation = Translation.objects.last()
        self.assertEqual(translation.text, 'Hello world!')
        self.assertEqual(translation.translated_text, 'Witaj świecie! Witaj świecie!')
        self.assertEqual(translation.user, self.user)

    def test_post_home_with_polish(self):
        count_before = Translation.objects.count()
        response = self.client.post(self.url, {'text': 'Witaj świecie!', 'language': 'Polish'})
        count_after = Translation.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Witaj świecie!', response.content.decode('utf-8'))
        self.assertInHTML('Hello world!', response.content.decode('utf-8'))
        self.assertEqual(count_after, count_before + 1)
        translation = Translation.objects.last()
        self.assertEqual(translation.text, 'Witaj świecie!')
        self.assertEqual(translation.translated_text, 'Hello world!')
        self.assertEqual(translation.user, None)

    def test_post_home_with_user(self):
        self.client.login(username=self.user.username, password='Password123')
        count_before = Translation.objects.count()
        response = self.client.post(self.url, {'text': 'Hello there!', 'language': 'English'})
        count_after = Translation.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Hello there!', response.content.decode('utf-8'))
        self.assertInHTML('Witajcie tutaj!', response.content.decode('utf-8'))
        self.assertEqual(count_after, count_before + 1)
        translation = Translation.objects.last()
        self.assertEqual(translation.text, 'Hello there!')
        self.assertEqual(translation.translated_text, 'Witajcie tutaj!')
        self.assertEqual(translation.user, self.user)

    def test_home_greets_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Welcome, guest!', response.content.decode('utf-8'))

    def test_home_greets_user(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertInHTML('Welcome, MichaelScott!', response.content.decode('utf-8'))
