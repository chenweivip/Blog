#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2017/11/22

from django import template
from django.utils.safestring import mark_safe
import time

register = template.Library()  # register的名字是固定的,不可改变


@register.filter
def filter_multi(v1,v2):
    return v2 - v1
