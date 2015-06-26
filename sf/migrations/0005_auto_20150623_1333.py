# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sf', '0004_page_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='slug',
        ),
        migrations.AlterField(
            model_name='page',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
