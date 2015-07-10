# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sf', '0005_auto_20150623_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content',
            field=models.CharField(max_length=305, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
