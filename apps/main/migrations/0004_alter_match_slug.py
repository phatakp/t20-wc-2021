# Generated by Django 3.2.8 on 2021-10-18 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211017_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
