# Generated by Django 3.0.6 on 2020-12-06 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_Socialite', '0004_auto_20201116_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='college_branch',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
