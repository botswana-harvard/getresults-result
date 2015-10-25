# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getresults_result', '0002_auto_20151025_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalresult',
            name='release_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicalresult',
            name='validation_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='release_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='validation_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
