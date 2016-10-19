# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scutmocc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nickname', models.CharField(max_length=10)),
                ('Sex', models.BooleanField()),
                ('Signature', models.CharField(max_length=100)),
                ('Zc_Date', models.DateField(auto_now_add=True)),
                ('Fb_sum', models.IntegerField()),
                ('Hf_sum', models.IntegerField()),
                ('Gz_sum', models.IntegerField()),
                ('Bgz_sum', models.IntegerField()),
                ('Sc_sum', models.IntegerField()),
                ('Rank', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]