# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_trans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='field_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together=set([('table_name', 'field_name', 'field_id', 'language')]),
        ),
    ]
