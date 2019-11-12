#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019-11-12


from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(name="add")
def add():
    return 2


@shared_task(name="reduce")
def reduce(x, y):
    return x - y
