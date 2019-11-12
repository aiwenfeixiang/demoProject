#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019-11-12

import os

from django.conf import settings

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otherDemo.settings")

app = Celery(
    "otherDemo",
    # broker=settings.CELERY_BROKER_URL,
    # backend=settings.CELERY_BROKER_URL
)

app.config_from_object("django.conf:settings")
# 设定时区
app.conf.timezone = settings.TIME_ZONE
app.autodiscover_tasks()
