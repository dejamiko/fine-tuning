from django.core.exceptions import ValidationError
from django.test import TestCase
from translate.models import User, Translation

"""Tests of the translation model."""


class TestTranslationModel(TestCase):
    fixtures = ['translate/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='MichaelScott')
        self.translation = Translation.objects.create(
            user=self.user,
            text='Hello',
            translated_text='Cześć',
            input_language='English'
        )
        self.translation.save()

    def test_translation_is_valid(self):
        self._assert_translation_is_valid()

    def test_original_text_cannot_be_blank(self):
        self.translation.text = ''
        self._assert_translation_is_invalid()

    def test_original_text_can_be_255_characters_long(self):
        self.translation.text = 'x' * 255
        self._assert_translation_is_valid()

    def test_original_text_cannot_be_more_than_255_characters_long(self):
        self.translation.text = 'x' * 256
        self._assert_translation_is_invalid()

    def test_translated_text_cannot_be_blank(self):
        self.translation.translated_text = ''
        self._assert_translation_is_invalid()

    def test_translated_text_can_be_255_characters_long(self):
        self.translation.translated_text = 'x' * 255
        self._assert_translation_is_valid()

    def test_translated_text_cannot_be_more_than_255_characters_long(self):
        self.translation.translated_text = 'x' * 256
        self._assert_translation_is_invalid()

    def test_user_can_be_null(self):
        self.translation.user = None
        self._assert_translation_is_valid()

    def test_input_language_cannot_be_blank(self):
        self.translation.input_language = ''
        self._assert_translation_is_invalid()

    def test_input_language_can_only_be_english_or_polish(self):
        self.translation.input_language = 'German'
        self._assert_translation_is_invalid()

    def _assert_translation_is_valid(self):
        try:
            self.translation.full_clean()
        except ValidationError:  # pragma: no cover
            self.fail('Test translation should be valid')

    def _assert_translation_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.translation.full_clean()
