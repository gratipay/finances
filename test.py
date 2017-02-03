#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess
import sys
import traceback
from os import path
from decimal import Decimal as D


# Helpers
# =======

root = path.realpath(path.dirname(__file__))

def report_balances():
    report = subprocess.check_output('bean-report gratipay.beancount balances', shell=True)
    for line in report.splitlines():
        if not line:
            break
        line = line.decode('utf8')
        splitted = line.split(None, 2)
        if len(splitted) == 3:
            yield splitted


# Tests
# =====

def test_escrow_balances():
    escrow_assets = escrow_liability = D(0)

    for account, amount, currency in report_balances():
        if account.startswith('Assets:Escrow:'):
            escrow_assets += D(amount)
        if account.startswith('Liabilities:Escrow'):
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
    subprocess.check_output('bean-check gratipay.beancount', shell=True)
    print('good')


if __name__ == '__main__':
    nfailures = 0
    filt = sys.argv[1] if len(sys.argv) > 1 else ''
    for name, test_func in list(globals().items()):
        if name.startswith('test_') and filt in name:
            print(name, "... ", end='')
            sys.stdout.flush()
            try:
                test_func()
            except:
                nfailures += 1
                traceback.print_exc()
                print()
    raise SystemExit(nfailures)
