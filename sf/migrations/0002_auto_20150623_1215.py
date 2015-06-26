# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True, default=datetime.datetime(2015, 6, 23, 12, 15, 50, 747264, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
