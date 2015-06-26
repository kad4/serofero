# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sf', '0003_remove_page_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True, default=datetime.datetime(2015, 6, 23, 12, 19, 10, 480976, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
