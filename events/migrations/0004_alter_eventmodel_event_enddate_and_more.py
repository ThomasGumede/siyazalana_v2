# Generated by Django 5.1.3 on 2024-06-17 22:20

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_eventmodel_event_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='event_enddate',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 6, 17, 22, 20, 8, 472266, tzinfo=datetime.timezone.utc), 'Event end date and time cannot be in the past')]),
        ),
        migrations.AlterField(
            model_name='eventmodel',
            name='event_startdate',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 6, 17, 22, 20, 8, 472183, tzinfo=datetime.timezone.utc), 'Event start date and time cannot be in the past')]),
        ),
        migrations.AlterField(
            model_name='eventtickettypemodel',
            name='sale_end',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 6, 17, 22, 20, 8, 480223, tzinfo=datetime.timezone.utc), 'Ticket sale end date and time cannot be in the past')]),
        ),
        migrations.AlterField(
            model_name='eventtickettypemodel',
            name='sale_start',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 6, 17, 22, 20, 8, 480157, tzinfo=datetime.timezone.utc), 'Ticket sale start date and time cannot be in the past')]),
        ),
    ]
