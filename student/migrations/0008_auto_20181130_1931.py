# Generated by Django 2.1.1 on 2018-11-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20181127_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='lecture_day',
            field=models.CharField(choices=[('MON', 'Monday'), ('TUES', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday')], max_length=10),
        ),
    ]
