# Generated by Django 3.2.8 on 2021-10-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_matchresult_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresult',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]
