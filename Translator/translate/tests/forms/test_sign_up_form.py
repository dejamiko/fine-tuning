from django.test import TestCase

from django import forms
from translate.forms import SignUpForm

"""Tests of the sign up form. The structure of the tests was inspired by the Clucker project from 5CCS2SEG."""


class TestSignUpForm(TestCase):
    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {
            'username': 'JimHalpert',
            'email': 'jimhalpert@dundermifflin.com',
            'password1': 'DwightIsTheBest123',
            'password2': 'DwightIsTheBest123'
        }

    def test_form_contains_required_fields(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        password1_field = form.fields['password1']
        password2_field = form.fields['password2']
        self.assertTrue(isinstance(password1_field.widget, forms.PasswordInput))
        self.assertTrue(isinstance(password2_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_form_rejects_blank_password1(self):
        self.form_input['password1'] = ''
        self.form_input['password2'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'], ['This field is required.'])

    def test_form_rejects_blank_password2(self):
        self.form_input['password2'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_form_rejects_passwords_that_do_not_match(self):
        self.form_input['password2'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_form_rejects_username_that_is_already_taken(self):
        self.form_input['username'] = 'MichaelScott'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['A user with that username already exists.'])

    def test_form_rejects_email_that_is_already_taken(self):
        self.form_input['email'] = 'michaelscott@dundermifflin.com'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['User with this Email already exists.'])

    def test_form_rejects_common_passwords(self):
        self.form_input['password1'] = 'password'
        self.form_input['password2'] = 'password'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['This password is too common.'])

    def test_form_rejects_passwords_that_are_too_short(self):
        self.form_input['password1'] = 'short'
        self.form_input['password2'] = 'short'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         ['This password is too short. It must contain at least 8 characters.'])

    def test_form_rejects_passwords_similar_to_username(self):
        self.form_input['password1'] = 'JimHalpert'
        self.form_input['password2'] = 'JimHalpert'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The password is too similar to the username.'])

    def test_form_rejects_passwords_similar_to_email(self):
        self.form_input['password1'] = 'dundermifflin.com'
        self.form_input['password2'] = 'dundermifflin.com'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The password is too similar to the email.'])
