#!/usr/bin/python3
# -*- coding:utf-8 -*-

import abc

class Step:

    def __init__(self):
        __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError
