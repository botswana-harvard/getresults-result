# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getresults_result', '0004_auto_20151028_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalresultitem',
            name='validation_comment',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resultitem',
            name='validation_comment',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalrelease',
            name='status',
            field=models.CharField(max_length=25, choices=[('release', 'Release'), ('review', 'Review')], blank=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='status',
            field=models.CharField(max_length=25, choices=[('release', 'Release'), ('review', 'Review')], blank=True),
        ),
    ]
