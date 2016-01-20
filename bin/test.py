#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function, unicode_literals

import commands
import sys
import traceback
from os import path
from decimal import Decimal as D


root = path.realpath(path.dirname(__file__))
report_scripts = { 'balance sheet': path.join(root, 'balance-sheet.py')
                 , 'income statement': path.join(root, 'income-statement.py')
                  }


def report(name):
    status, report = commands.getstatusoutput(report_scripts[name] + ' --flat')
    if status > 0:
        raise SystemExit(report)
    for line in report.splitlines():
        yield line.strip()


def test_escrow_balances():
    escrow_assets = escrow_liability = D(0)

    for line in report('balance sheet'):
        if line.startswith('------------') or not line: break
        currency, amount, account = line.split(None, 2)
        if account.startswith('Assets:Escrow:'):
            escrow_assets += D(amount)
        if account.startswith('Liabilities:Escrow'):
            escrow_liability += D(amount)

    print(escrow_assets, escrow_liability)
    assert escrow_assets + escrow_liability == 0


def test_fee_buffer_reconciles_with_fees():

    fee_income = fee_expense = fee_buffer = D(0)

    for line in report('balance sheet'):
        if line.startswith('------------') or not line: break
        currency, amount, account = line.split(None, 2)
        if account.startswith('Assets:Fee Buffer:'):
            fee_buffer += D(amount)

    for line in report('income statement'):
        if line.startswith('------------') or not line: break
        currency, amount, account = line.split(None, 2)
        if account.startswith('Income:Processing:Fees:'):
            fee_income -= D(amount)
        if account.startswith('Expenses:Processing:Fees:'):
            fee_expense -= D(amount)

    delta = fee_income + fee_expense
    print(fee_income, fee_expense, delta, fee_buffer, abs(delta-fee_buffer))
    assert delta == fee_buffer


def test_net_income_reconciles_with_retained_earnings():

    retained_earnings = net_income = D(0)

    for line in report('balance sheet'):
        if line.startswith('------------') or not line: break
        currency, amount, account = line.split(None, 2)
        if account == 'Equity:Retained Earnings':
            retained_earnings = D(amount)
            break

    for line in report('income statement'):
        if not line or ':' in line or line.startswith('------------'): continue
        currency, total = line.split()
        net_income = D(total)
        break

    print(retained_earnings, net_income)
    assert retained_earnings == net_income


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
