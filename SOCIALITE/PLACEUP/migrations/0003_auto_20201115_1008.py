# Generated by Django 3.0.6 on 2020-11-15 18:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PLACEUP', '0002_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='about',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='work',
            name='min_requirement',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
