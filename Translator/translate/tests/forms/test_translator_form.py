from django.test import TestCase

from translate.forms import TranslatorForm

"""Tests of the translator form."""


class TestTranslatorForm(TestCase):
    def setUp(self):
        self.form_input = {
            'text': 'Hello World',
            'language': 'English'
        }

    def test_form_contains_required_fields(self):
        form = TranslatorForm()
        self.assertIn('text', form.fields)
        self.assertIn('language', form.fields)

    def test_form_accepts_valid_input(self):
        form = TranslatorForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_text(self):
        self.form_input['text'] = ''
        form = TranslatorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['This field is required.', 'Please enter some text.'])

    def test_form_rejects_blank_language(self):
        self.form_input['language'] = ''
        form = TranslatorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['language'], ['This field is required.'])
