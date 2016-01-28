#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from os import path

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

reporting.income_statement()
