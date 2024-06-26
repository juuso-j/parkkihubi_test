# Generated by Django 2.2.15 on 2023-11-02 12:08

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0046_add_eventarea'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventParking',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='time created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='time modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(
                    blank=True, null=True, srid=4326, verbose_name='location')),
                ('registration_number', models.CharField(db_index=True, max_length=20, verbose_name='registration number')),
                ('normalized_reg_num', models.CharField(db_index=True,
                                                        max_length=20, verbose_name='normalized registration number')),
                ('time_start', models.DateTimeField(db_index=True, verbose_name='parking start time')),
                ('time_end', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='parking end time')),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                             related_name='event_parkings', to='parkings.EnforcementDomain')),
                ('event_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 related_name='event_parkings', to='parkings.EventArea', verbose_name='event area')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                               related_name='event_parkings', to='parkings.Operator', verbose_name='operator')),
            ],
            options={
                'verbose_name': 'event parking',
                'verbose_name_plural': 'event parkings',
                'default_related_name': 'event_parkings',
            },
        ),
    ]
