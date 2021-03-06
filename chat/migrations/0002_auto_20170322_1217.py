# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 12:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.UserGroup'),
        ),
    ]
