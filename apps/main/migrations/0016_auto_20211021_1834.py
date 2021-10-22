# Generated by Django 3.2.8 on 2021-10-21 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20211021_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='match',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.match'),
        ),
        migrations.AlterField(
            model_name='standing',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.team'),
        ),
    ]
