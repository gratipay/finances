#!/usr/bin/env python2
"""Given a Stripe payments CSV export, sum the fees.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import csv, sys
from decimal import Decimal as D

inp = csv.reader(open(sys.argv[1]))
headers = next(inp)

fees = D(0)

for row in inp:
    rec = dict(zip(headers, row))
    fees += D(rec['Fee'])

print(fees)
