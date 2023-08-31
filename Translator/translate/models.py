from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A simple user model that extends the default Django user model."""
    email = models.EmailField(max_length=254, unique=True)


class Translation(models.Model):
    """A translation of a word or phrase."""

    class LanguageChoices(models.TextChoices):
        ENGLISH = 'English'
        POLISH = 'Polish'

    text = models.CharField(max_length=255)
    translated_text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    input_language = models.CharField(max_length=7, choices=LanguageChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def text_display(self):
        return self.text[:27] + '...' if len(self.text) > 30 else self.text

    def translated_text_display(self):
        return self.translated_text[:27] + '...' if len(self.translated_text) > 30 else self.translated_text
