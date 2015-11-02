# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getresults_result', '0005_auto_20151030_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalresultitem',
            name='validated',
        ),
        migrations.RemoveField(
            model_name='resultitem',
            name='validated',
        ),
        migrations.AddField(
            model_name='historicalresultitem',
            name='comment',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalresultitem',
            name='release_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalresultitem',
            name='release_status',
            field=models.CharField(max_length=10, null=True, choices=[('release', 'Release'), ('review', 'Review')]),
        ),
        migrations.AddField(
            model_name='resultitem',
            name='comment',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resultitem',
            name='release_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resultitem',
            name='release_status',
            field=models.CharField(max_length=10, null=True, choices=[('release', 'Release'), ('review', 'Review')]),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='release_status',
            field=models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('repeated', 'Repeated'), ('cancelled', 'Cancelled')]),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='status',
            field=models.CharField(max_length=10, default='pending', choices=[('accept', 'Accept'), ('repeat', 'Repeat'), ('cancel', 'Cancel'), ('ignore', 'Ignore'), ('pending', 'Pending')]),
        ),
        migrations.AlterField(
            model_name='result',
            name='release_status',
            field=models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('repeated', 'Repeated'), ('cancelled', 'Cancelled')]),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='status',
            field=models.CharField(max_length=10, default='pending', choices=[('accept', 'Accept'), ('repeat', 'Repeat'), ('cancel', 'Cancel'), ('ignore', 'Ignore'), ('pending', 'Pending')]),
        ),
    ]
