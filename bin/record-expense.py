#!/usr/bin/env python2
"""Add an expense to the .dat for the current month

CMD    : $ record-expense.py github 14.95 2016-12-01
Expect : $ Expense Recorded 

# TODO 
# 1. Validate Date and Amount
# 2. Add functionality to record more types of expenses
# 3. When 2 is implemented validate against declareation.dat

"""

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
from decimal import InvalidOperation, Decimal as D
import sys

EXPENSE = """

{Date}  {Payee}
    Expense:Operations:SAS                          ${amount:10}                      
    Asset:Operations:PNC                           -${amount:10} 
{Date}  Current Activity
    Equity:Current Activity                         ${amount:10}
    Expenses:Operations:SAS                        -${amount:10}

"""

if len(sys.argv) < 3:
    raise SystemExit("""
                        Usage: record-expense.py <payee> <amount> [date]
                        NB: Date must be in the format yyyy-mm-dd
                        NB: Amount must be a valid monetary amount without the dollar sign 
                     """)

today = datetime.now()

if len(sys.argv) == 3:
    date = today.strftime('%Y-%m-%d')
else: 
    date= sys.argv[3]

month = today.month
year = today.year

if month < 6:
    folder = 'FY%s' %  (year)
else:
    folder = 'FY%s' % (year+1)

payee = sys.argv[1]
amount = sys.argv[2]


try:
    D(amount)
except InvalidOperation:
    raise SystemExit("Please enter a valid monetary value with out the dollar sign")

dat_file = '%s/%d-%d.dat' % (folder, year, month)

template = EXPENSE 


with open(dat_file, 'a') as f:
    f.write(template.format(**dict(Date=date, Payee=sys.argv[1], amount=sys.argv[2])))

print (template.format(**dict(Date=date, Payee=sys.argv[1], amount=sys.argv[2])))
