from django.test import TestCase

from django import forms
from translate.forms import LogInForm

"""Tests of the log in form. The structure of the tests was inspired by the Clucker project from 5CCS2SEG."""


class TestLogInForm(TestCase):
    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self) -> None:
        self.form_input = {'username': 'MichaelScott', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'DwightSchrute'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'WrongPassword123'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_can_authenticate_valid_user(self):
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user.username, 'MichaelScott')

    def test_invalid_credentials_do_not_authenticate(self):
        self.form_input['password'] = 'WrongPassword123'
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_password_do_not_authenticate(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_username_do_not_authenticate(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user, None)
