# Generated by Django 2.1.1 on 2018-11-22 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20181122_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='lecture_day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday')]),
        ),
    ]
