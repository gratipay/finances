#!/usr/bin/env python2.7 -u
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


def report(name, just_accounts=False):
    status, report = commands.getstatusoutput(report_script(name) + ' --flat')
    if status > 0:
        raise SystemExit(report)
    for line in report.splitlines():
        if just_accounts:
            if line.startswith('------------') or not line: break
            yield line.split(None, 2)
        else:
            yield line.strip()


def accounts(name):
    return report(name, just_accounts=True)


def account(report, target_account):
    total = D(0)
    for currency, amount, account in accounts('balance sheet'):
        if account == target_account:
            total += D(amount.replace(',', ''))
    return total


def total(name):
    total = D(0)
    for line in report(name):
        if line.startswith('$'):
            try:
                currency, total, _ = line.split(None, 2)
            except ValueError:
                currency, total = line.split()
                break
            total = D(total.replace(',', ''))
    return total


# Tests
# =====

def test_escrow_balances():
    escrow_assets = escrow_liability = D(0)

    for currency, amount, account in accounts('balance sheet'):
        if account.startswith('Assets:Escrow:'):
            escrow_assets += D(amount)
        if account.startswith('Liabilities:Escrow'):
            escrow_liability += D(amount)

    print(escrow_assets, escrow_liability)
    assert escrow_assets + escrow_liability == 0


def test_fee_buffer_balances():
    fee_buffer_assets = fee_buffer_liability = D(0)

    for currency, amount, account in accounts('balance sheet'):
        if account.startswith('Assets:Fee Buffer:'):
            fee_buffer_assets += D(amount)
        if account.startswith('Liabilities:Fee Buffer'):
            fee_buffer_liability += D(amount)

    print(fee_buffer_assets, fee_buffer_liability)
    assert fee_buffer_assets + fee_buffer_liability == 0


def test_income_balances():
    for currency, amount, account in accounts('balance sheet'):
        assert not account.startswith('Income:')
    print('good')


def test_expenses_balance():
    for currency, amount, account in accounts('balance sheet'):
        assert not account.startswith('Expenses:')
    print('good')


def test_fee_buffer_income_reconciles_with_fee_buffer_liability():
    net_fee_income = total('fee buffer statement')
    fee_buffer = account('balance sheet', 'Liabilities:Fee Buffer')
    print(net_fee_income, fee_buffer)
    assert net_fee_income == fee_buffer


def test_net_income_reconciles_with_current_activity():
    net_income = total('income statement')
    current_activity = account('balance sheet', 'Equity:Current Activity')
    print(net_income, current_activity)
    assert net_income == current_activity


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
