# Generated by Django 3.0.6 on 2020-11-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_Socialite', '0004_auto_20201116_0722'),
        ('PLACEUP', '0005_work_resume_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='hired',
            field=models.ManyToManyField(related_name='hired', to='Django_Socialite.Profile'),
        ),
    ]