# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getresults_result', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalresultitem',
            name='validation_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='resultitem',
            name='validation_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
