# Generated by Django 3.2.8 on 2021-10-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20211020_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[(None, '----'), ('completed', 'Completed'), ('abandoned', 'Abandoned')], db_index=True, default='scheduled', max_length=20),
        ),
        migrations.AlterField(
            model_name='matchresult',
            name='win_type',
            field=models.CharField(blank=True, choices=[('wickets', 'wickets'), ('runs', 'runs')], max_length=10, null=True),
        ),
    ]