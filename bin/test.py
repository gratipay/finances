#!/usr/bin/env python -u
from __future__ import absolute_import, division, print_function, unicode_literals

import commands
import sys
import traceback
from os import path
from decimal import Decimal as D


# Helpers
# =======

root = path.realpath(path.dirname(__file__))
report_script = lambda a: path.join(root, a.replace(' ', '-') + '.py')

def report_balances():
    status, report = commands.getstatusoutput('bean-report FY2013/FY2013.beancount balances')
    for line in report.splitlines():
        if not line:
            break
        else:
            splited = line.split(None, 2)
            if (len(splited) == 3):
                yield splited


# Tests
# =====

def test_escrow_balances():
    escrow_assets = escrow_liability = D(0)

    for account, amount, currency in report_balances():
        if account.startswith('Assets:Escrow:'):
            #print(account, amount)
            escrow_assets += D(amount)
        if account.startswith('Liabilities:Escrow'):
            #print(account, amount)
            escrow_liability += D(amount)

    print(escrow_assets, escrow_liability)
    assert escrow_assets + escrow_liability == 0


def test_fee_buffer_balances():
    fee_buffer_assets = fee_buffer_liability = D(0)

    for account, amount, currency in report_balances():
        if account.startswith('Assets:Fee-Buffer:'):
            fee_buffer_assets += D(amount)
        if account.startswith('Liabilities:Fee-Buffer'):
            fee_buffer_liability += D(amount)

    print(fee_buffer_assets, fee_buffer_liability)
    assert fee_buffer_assets + fee_buffer_liability == 0


def test_beancount_check():
    status, report = commands.getstatusoutput('bean-check FY2013/FY2013.beancount')
    if report != '':
        raise SystemExit(report)
    else:
        print('good')

if __name__ == '__main__':
    nfailures = 0
    filt = sys.argv[1] if len(sys.argv) > 1 else ''
    for name, test_func in globals().items():
        if name.startswith('test_') and filt in name:
            print(name, "... ", end='')
            try:
                test_func()
            except:
                nfailures += 1
                traceback.print_exc()
                print()
    raise SystemExit(nfailures)
