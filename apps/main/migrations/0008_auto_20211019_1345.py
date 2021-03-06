# Generated by Django 3.2.8 on 2021-10-19 08:15

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_match_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='team1_score',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[main.validators.score_validator]),
        ),
        migrations.AlterField(
            model_name='matchresult',
            name='team2_score',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[main.validators.score_validator]),
        ),
    ]
