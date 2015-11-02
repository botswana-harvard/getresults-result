# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getresults_result', '0003_auto_20151025_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrelease',
            name='comment',
            field=models.CharField(max_length=25, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalrelease',
            name='status',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='last_exported_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='release_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='release_status',
            field=models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='status',
            field=models.CharField(max_length=1, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='validation_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='validation_status',
            field=models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('validated', 'Validated'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='status',
            field=models.CharField(max_length=10, choices=[('accept', 'Accept'), ('repeat', 'Repeat'), ('cancel', 'Cancel'), ('ignore', 'Ignore')], null=True),
        ),
        migrations.AlterField(
            model_name='historicalvalidate',
            name='comment',
            field=models.CharField(max_length=25, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='comment',
            field=models.CharField(max_length=25, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='status',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='result',
            name='last_exported_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='release_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='release_status',
            field=models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='result',
            name='status',
            field=models.CharField(max_length=1, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='validation_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='validation_status',
            field=models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('validated', 'Validated'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='status',
            field=models.CharField(max_length=10, choices=[('accept', 'Accept'), ('repeat', 'Repeat'), ('cancel', 'Cancel'), ('ignore', 'Ignore')], null=True),
        ),
        migrations.AlterField(
            model_name='validate',
            name='comment',
            field=models.CharField(max_length=25, blank=True, null=True),
        ),
    ]
