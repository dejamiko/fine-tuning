from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from translate.models import User

import translator_backend


class LogInForm(forms.Form):
    """Form to log in users. Adapted from the Clucker project from 5CCS2SEG."""
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def get_user(self):
        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password1')
        password_confirmation = self.cleaned_data.get('password2')
        if password != password_confirmation:
            self.add_error('password1', 'Confirmation does not match password.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class TranslatorForm(forms.Form):
    language = forms.ChoiceField(label='Input language', choices=[('English', 'English'), ('Polish', 'Polish')])
    text = forms.CharField(label='Text',
                           widget=forms.Textarea(attrs={'rows': 10, 'cols': 50, 'placeholder': 'Enter text here'}))

    def clean(self):
        super().clean()
        text = self.cleaned_data.get('text')
        if not text:
            self.add_error('text', 'Please enter some text.')

    def translate(self):
        text = self.cleaned_data.get('text')
        if self.cleaned_data['language'] == 'English':
            translated_texts = translator_backend.translateEnglishToPolish(text)
        else:
            translated_texts = translator_backend.translatePolishToEnglish(text)
        whole_text = []
        for translated_text in translated_texts:
            whole_text.append(translated_text['translation_text'])
        return '\n'.join(whole_text)
