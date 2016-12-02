#!/usr/bin/env python2
"""Add an expense to the .dat for the current month

CMD    : $ record-expense.py Software Github 14.95 2016-12-01

"""

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
from decimal import InvalidOperation, Decimal as D
import sys

template = """

{date}  {payee}
    {exp_account:50}${amount:10}                      
    Asset:Operations:PNC                             -${amount:10} 
{date}  Current Activity 
    Equity:Current Activity                           ${amount:10}
    {exp_account:49}-${amount:10}                      
"""

if len(sys.argv) < 4:
    raise SystemExit("""Usage: record-expense.py <account> <payee> <amount> [date]
                        NB: Date must be in the format yyyy-mm-dd
                        NB: Amount must be a valid monetary amount without the dollar sign 
                     """)

account = sys.argv[1]
payee = sys.argv[2]
amount = sys.argv[3]

try:
    D(amount)
except InvalidOperation:
    raise SystemExit("\nPlease enter a valid monetary value with out the dollar sign\n")

today = datetime.now()
if len(sys.argv) == 4:
    date = today.strftime('%Y-%m-%d')
else: 
    date = sys.argv[4]
    try:
        datetime.strptime(date,'%Y-%m-%d')
    except ValueError:
        raise SystemExit("\nIncorrect date format. Should be yyyy-mm-dd\n")

month = today.month
year = today.year

if month < 6:
    folder = 'FY%s' %  (year)
else:
    folder = 'FY%s' % (year+1)

exp_account = ''
with open('%s/declarations.dat' % folder, 'r') as declared:
    for line in declared:
        if account in line:
            exp_account = line.split(' ')[1].rstrip()

if not exp_account:
    raise SystemExit("\nThe Expense account entered is invalid for this Fiscal year\n") 

dat_file = '%s/%d-%d.dat' % (folder, year, month)

with open(dat_file, 'a') as f:
    f.write(template.format(**dict( exp_account=exp_account
                                  , date=date
                                  , payee=payee
                                  , amount=amount
                                  )
                           )
           )

print(template.format(**dict( exp_account=exp_account
                            , date=date
                            , payee=payee
                            , amount=amount
                            )
                     )
     )
