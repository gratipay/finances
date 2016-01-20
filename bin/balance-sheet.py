#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from os import path
import calendar

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

cmd = [ 'ledger'
      , 'balance'
      , '--sort "account =~ /^Assets.*/ ? 0 : '
      ,        '(account =~ /^Liabilities.*/ ? 1 : '
      ,        '(account =~ /^Equity.*/ ? 2 : 3)))"'
       ]
cmd += sys.argv[1:]

year, month = reporting.parse(sys.argv[1:])[1]

# Each year opens with a carryover balance, so we don't have to go further back than that.
start = [year, None]
end = [year, month]
for datfile in reporting.list_datfiles(start, end):
    cmd.append('-f {}'.format(datfile))

print()
print("BALANCE SHEET".center(42))
print("as of {} {}, {}".format( calendar.month_name[int(end[1])]
                              , calendar.monthrange(int(end[0]), int(end[1]))[1]
                              , end[0]
                               ).center(42))
print()
os.system(' '.join(cmd))
