# Generated by Django 4.1.5 on 2023-02-02 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('translate', '0002_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
