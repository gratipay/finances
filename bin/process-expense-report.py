#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import sys


EXPENSE = """\
{Date}  {Payee}
    {Expense Account:64}${Amount:>10}
    {Asset Account:63}-${Amount:>10}
{Date}  Current Activity
    {Liability Account:64}${Amount:>10}
    {Expense Account:63}-${Amount:>10}"""

TRANSFER = """\
{Date}  {Payee}
    {To Account:64}${Amount:>10}
    {From Account:63}-${Amount:>10}"""


def main():
    expenses = csv.reader(sys.stdin)
    headers = expenses.next()
    for row in expenses:
        data = dict(zip(headers, row))

        notes = data.pop('Notes')

        if data['Account'].startswith('Expenses:'):
            tmpl = EXPENSE
            data['Expense Account'] = data.pop('Account')
            data['Asset Account'] = 'Assets:Operations:PNC'
            data['Liability Account'] = 'Equity:Current Activity'
        else:
            tmpl = TRANSFER
            data['From Account'] = 'Assets:Operations:PNC'
            data['To Account'] = data.pop('Account')

        if notes:
            print('; ' + notes)
        print(tmpl.format(**data))
        print()

    data = {}


if __name__ == '__main__':
    main()
