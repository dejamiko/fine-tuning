from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from translate.forms import SignUpForm
from translate.models import User
from translate.tests.helpers import LogInTester

"""Tests of the sign up view. The structure of the tests was inspired by the clucker project from 5CCS2SEG."""


class SignUpViewTestCase(TestCase, LogInTester):
    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('signup')
        self.user = User.objects.get(username='MichaelScott')
        self.form_input = {
            'username': 'DwightSchrute',
            'email': 'dwightschrute@dundermifflin.com',
            'password1': 'JimHalpertIsTheBest123',
            'password2': 'JimHalpertIsTheBest123'
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/signup/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['username'] = 'BAD USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'home.html')

        user = User.objects.get(username='DwightSchrute')
        self.assertEqual(user.email, 'dwightschrute@dundermifflin.com')
        is_password_correct = check_password(self.form_input['password1'], user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    def test_get_sign_up_redirects_to_home_when_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('home')
        self.assertTemplateUsed(response, 'home.html')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_sign_up_redirects_to_home_when_logged_in(self):
        before_count = User.objects.count()
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('home')
        self.assertTemplateUsed(response, 'home.html')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
