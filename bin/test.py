#!/usr/bin/env python2
import commands
from os import path
from decimal import Decimal as D

root = path.realpath(path.dirname(__file__))
balance_script = path.join(root, 'balance-sheet.py')


def test_escrow_balances():
    balance_sheet = commands.getoutput(balance_script + ' --flat')

    escrow_assets = escrow_liability = D(0)

    for line in balance_sheet.splitlines():
        line = line.strip()
        if line.startswith('------------'): break
        currency, amount, account = line.split(None, 2)
        if 'Assets:Escrow' in account:
            escrow_assets += D(amount)
        if 'Liabilities:Escrow' in account:
            escrow_liability += D(amount)

    assert escrow_assets + escrow_liability == 0, (escrow_assets, escrow_liability)


if __name__ == '__main__':
    for name, test_func in globals().items():
        if name.startswith('test_'):
            test_func()
