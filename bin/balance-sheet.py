#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from os import path

base = path.realpath(path.join(path.dirname(__file__), '..'))
cmd = [ 'ledger'
      , 'balance'
      , '--sort "account =~ /Assets.*/ ? 0 : '
      ,        '(account =~ /Liabilities.*/ ? 1 : '
      ,        '(account =~ /Equity.*/ ? 2 : 3)))"'
       ]

years = [y for y in sorted(os.listdir(base)) if y.isdigit()]
year = years[-1]
month = None

if len(sys.argv) > 1:
    as_of = sys.argv[1].split('-')
    if len(as_of) == 1:
        as_of.append(month)
    year, month = as_of

if year not in years:
    sys.exit("Sorry, don't have that year.")

yeardir = path.join(base, year)
for filename in sorted(os.listdir(yeardir)):
    if not filename.endswith('.dat'): continue
    cmd.append('-f {}'.format(path.join(yeardir, filename)))
    latest_month = filename[:2]
    if latest_month == month:
        break

if month and latest_month != month:
    sys.exit("Sorry, don't have that month.")

print()
print("BALANCE SHEET".center(41))
print("as of {}-{}".format(year, latest_month).center(41))
print()
os.system(' '.join(cmd))
