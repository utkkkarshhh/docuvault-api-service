# Generated by Django 5.1.7 on 2025-06-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_auto_20250530233546'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_o_auth',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
