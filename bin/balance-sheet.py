#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from os import path

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

cmd = [ 'ledger'
      , 'balance'
      , '--sort "account =~ /^Assets.*/ ? 0 : '
      ,        '(account =~ /^Liabilities.*/ ? 1 : '
      ,        '(account =~ /^Equity.*/ ? 2 : 3)))"'
       ]

nargs = len(sys.argv[1:])
if nargs == 0:
    year = month = None
elif nargs == 1:
    year, month = reporting.parse(sys.argv[1])
else:
    sys.exit("Too many arguments.")

# Each year opens with a carryover balance, so we don't have to go further back than that.
start = [year, None]
end = [year, month]
for datfile in reporting.list_datfiles(start, end):
    cmd.append('-f {}'.format(datfile))

print()
print("BALANCE SHEET".center(41))
print("as of {}-{}".format(*end).center(41))
print()
os.system(' '.join(cmd))
