# Generated by Django 3.0.6 on 2020-11-13 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_type', models.CharField(max_length=30)),
                ('company_specialization', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20)),
                ('company_logo', models.ImageField(upload_to='company_logo')),
                ('about_company', models.TextField(max_length=300)),
                ('company_site', models.CharField(max_length=50)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
