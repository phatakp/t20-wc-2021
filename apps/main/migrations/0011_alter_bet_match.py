# Generated by Django 3.2.8 on 2021-10-20 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_matchresult_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_bets', to='main.matchresult'),
        ),
    ]
