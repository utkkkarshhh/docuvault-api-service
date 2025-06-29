# Generated by Django 5.1.7 on 2025-05-30 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=55, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('is_subscribed_to_emails', models.BooleanField(default=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('reason_for_deletion', models.CharField(blank=True, max_length=255, null=True)),
                ('deleted_at', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upload_limit_count', models.IntegerField(default=6)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.users')),
            ],
            options={
                'db_table': 'user_limit',
            },
        ),
        migrations.CreateModel(
            name='UserActiveToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.users')),
            ],
            options={
                'db_table': 'user_active_tokens',
            },
        ),
    ]
