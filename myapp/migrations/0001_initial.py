# Generated by Django 5.0.7 on 2024-07-28 14:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_region', models.CharField(max_length=100)),
                ('user_country_code', models.CharField(max_length=10)),
                ('user_country', models.CharField(max_length=100)),
                ('user_cadre', models.CharField(max_length=100)),
                ('access_permission', models.CharField(max_length=100)),
                ('added_by', models.CharField(max_length=100)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DynamicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_data', to='myapp.userprofile')),
            ],
        ),
    ]
