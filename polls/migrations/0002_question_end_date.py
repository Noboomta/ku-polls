# Generated by Django 3.1 on 2020-09-15 15:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 15, 12, 46, 909599, tzinfo=utc), verbose_name='data vote ended'),
            preserve_default=False,
        ),
    ]