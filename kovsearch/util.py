#! /usr/bin/env python
# coding:utf-8


import datetime
import logging


class Time:
    def __init__(self, format="time: "):
        self._format = format
    
    def __enter__(self):
        self._start = datetime.datetime.now()
    
    def __exit__(self, type, value, traceback):
        self._end = datetime.datetime.now()
        interval = self._end - self._start
        logging.info("{}{}".format(self._format, interval))