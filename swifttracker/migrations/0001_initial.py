# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('position', models.CharField(choices=[('developer', 'developer'), ('designer', 'designer')], default='', max_length=120)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(max_length=120)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('position', models.CharField(choices=[('developer', 'developer'), ('designer', 'designer')], max_length=1000)),
                ('weekly_hours', models.IntegerField()),
                ('username', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyReport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('date_track', models.DateField()),
                ('question1', models.CharField(max_length=2000)),
                ('question2', models.CharField(max_length=2000)),
                ('question3', models.CharField(max_length=2000)),
                ('time_track', models.CharField(max_length=2000)),
                ('project_name', models.ForeignKey(to='swifttracker.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
