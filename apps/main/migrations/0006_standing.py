# Generated by Django 3.2.8 on 2021-10-18 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20211018_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played', models.PositiveSmallIntegerField(default=0)),
                ('won', models.PositiveSmallIntegerField(default=0)),
                ('lost', models.PositiveSmallIntegerField(default=0)),
                ('no_result', models.PositiveSmallIntegerField(default=0)),
                ('points', models.PositiveSmallIntegerField(default=0)),
                ('nrr', models.FloatField(default=0)),
                ('for_runs', models.PositiveSmallIntegerField(default=0)),
                ('for_overs', models.FloatField(default=0)),
                ('against_runs', models.PositiveSmallIntegerField(default=0)),
                ('against_overs', models.FloatField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_standings', to='main.team')),
            ],
            options={
                'ordering': ('-points', '-nrr'),
            },
        ),
    ]
