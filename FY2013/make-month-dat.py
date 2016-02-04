#!/usr/bin/env python2
"""Make a dat file for a month, given a directory containing input CSVs.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import sys
from os import path

if len(sys.argv) != 2:
    raise SystemExit("usage: {} ../path/to/csv/root".format(sys.argv[0]))

csv_root = sys.argv[1]
csv_root = path.realpath(csv_root)

fy_root = path.realpath(path.dirname(__file__))


class TransactionBase(dict):
    def __init__(self, raw):
        dict.__init__(self)
        self._raw = raw
        self.update(raw)
        self.update(self.process(raw))

    def process(self, raw):
        processed = {}
        processed['Date'] = '{2:>04}-{0:>02}-{1:>02}'.format(*raw['Date'].split('/'))
        processed['Payee']
        return processed


EXPENSE = """
{Date}  {Payee}
    {Expense Account:63}$     0.08
    {Asset Account:63}-$     0.08
{Date}  Balance Sheet
    {Liability Account:63}$     0.08
    {Expense Account:63}-$     0.08"""

PAYDAY = """
{Date}  Settlement
    Assets:Escrow:New Alliance                                      $    20.67
    Assets:Fee Buffer:New Alliance                                  $     0.30
    Assets:Fee Buffer:Stripe                                       -$     0.30
    Assets:Escrow:Stripe                                           -$    20.67"""

SETTLEMENT = """
{Date}  Settlement
    Assets:Escrow:New Alliance                                      $    20.67
    Assets:Fee Buffer:New Alliance                                  $     0.30
    Assets:Fee Buffer:Stripe                                       -$     0.30
    Assets:Escrow:Stripe                                           -$    20.67"""


new_alliance = csv.DictReader(open(path.join(csv_root, 'new-alliance.csv')))

for row in new_alliance:
    template = None

    row['Date'] = '{2:>04}-{0:>02}-{1:>02}'.format(*row['Date'].split('/'))
    row['Amount'] = row['Amount'].replace('$', '')
    row['Account'] = ''

    blob = row['Description']
    if blob.startswith('EFT'):
        kind, payee = blob.split(' - ')

        if payee.startswith('MERCHANT BANKCD '):
            payee = 'Samurai'
        elif payee.startswith('AMERICAN EXPRESS '):
            payee = 'Samurai'
        elif payee.startswith('STRIPE '):
            payee = 'Stripe'

        row['Payee'] = payee

        if kind == 'EFT W/D':
            template = EXPENSE
            row['Expense Account'] = 'Expenses:Fee Buffer:' + payee
            row['Asset Account'] = 'Assets:Fee Buffer:New Alliance'
            row['Liability Account'] = 'Liabilities:Fee Buffer:'


    if template is None:
        print(row, file=sys.stderr)
    else:
        print(template.format(**row))
