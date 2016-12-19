#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class BillyBob:

    def __init__(self, **kargs):
        self._params = kargs

    def print_params(self):
        for param in self._params:
            print '{0}={1}'.format(param, self._params[param])
