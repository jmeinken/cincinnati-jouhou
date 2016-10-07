# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 18:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('microfeed', '0003_auto_20161004_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image_path', models.CharField(max_length=30)),
                ('order', models.IntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='microfeed.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
