# Generated by Django 3.0.6 on 2020-11-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_Socialite', '0002_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='college_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='college_year',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
