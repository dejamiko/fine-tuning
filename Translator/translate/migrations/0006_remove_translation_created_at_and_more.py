# Generated by Django 4.1.5 on 2023-02-09 15:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('translate', '0005_translation_input_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='updated_at',
        ),
    ]