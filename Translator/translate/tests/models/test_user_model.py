from django.core.exceptions import ValidationError
from django.test import TestCase
from translate.models import User

"""Tests of the user model. The structure of the tests was inspired by the clucker project from 5CCS2SEG."""


class TestUserModel(TestCase):
    fixtures = ['translate/tests/fixtures/default_user.json', 'translate/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='MichaelScott')

    def test_user_is_valid(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        dwight = User.objects.get(username='DwightSchrute')
        self.user.username = dwight.username
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        dwight = User.objects.get(username='DwightSchrute')
        self.user.email = dwight.email
        self._assert_user_is_invalid()

    def test_username_can_be_150_characters_long(self):
        self.user.username = 'x' * 150
        self.test_user_is_valid()

    def test_username_cannot_be_more_than_150_characters_long(self):
        self.user.username = 'x' * 151
        self._assert_user_is_invalid()

    def test_email_must_contain_an_at(self):
        self.user.email = 'michaelscottdundermifflin.com'
        self._assert_user_is_invalid()

    def test_email_must_contain_a_dot_in_the_domain(self):
        self.user.email = 'michaelscott@dundermifflincom'
        self._assert_user_is_invalid()

    def test_email_can_be_254_characters_long(self):
        self.user.email = 'x' * (254 - len("@dundermifflin.com")) + "@dundermifflin.com"
        self._assert_user_is_valid()

    def test_email_cannot_be_longer_than_254_characters_long(self):
        self.user.email = 'x' * (255 - len("@dundermifflin.com")) + "@dundermifflin.com"
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:  # pragma: no cover
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
