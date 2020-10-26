# Generated by Django 3.1.2 on 2020-10-26 17:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20201022_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='display_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 26, 17, 39, 55, 479570, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_acquired',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 10, 26, 17, 39, 55, 478555, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='last_inspected',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 26, 17, 39, 55, 478583, tzinfo=utc)),
        ),
    ]
