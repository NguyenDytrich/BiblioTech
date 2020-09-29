# Generated by Django 3.1.1 on 2020-09-28 21:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equilizer', '0006_auto_20200928_2147'),
    ***REMOVED***

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='member',
        ),
        migrations.AddField(
            model_name='checkout',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checkout',
            name='approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approver_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 28, 21, 51, 52, 617747, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_acquired',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 9, 28, 21, 51, 52, 616904, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='last_inspected',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 28, 21, 51, 52, 616931, tzinfo=utc)),
        ),
    ***REMOVED***