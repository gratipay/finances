"""This is a library to support Gratipay's financial reporting.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import calendar
import subprocess
import re
import sys
from os import chdir, getcwd, listdir, path
from collections import defaultdict


FISCAL_YEAR_STARTING_MONTH = '06'


def parse(argv):
    """Given a command-line argument vector, return a (year, month) tuple.

    Raises SystemExit if the argument is in a bad format.

    """
    parser = argparse.ArgumentParser(argument_default='')
    parser.add_argument('-b', '--begin', default='')
    parser.add_argument('-e', '--end', default='')
    date_range, _ = parser.parse_known_args(argv)
    return (parse_one(date_range.begin), parse_one(date_range.end))


def parse_one(arg):
    patterns = (r'^\d\d\d\d-\d\d-\d\d', r'^\d\d\d\d-\d\d$', r'^\d\d\d\d$', r'^\d\d$')
    if arg and not any([re.match(p, arg) for p in patterns]):
        sys.exit("Bad argument, must be YYYY-MM-DD, YYYY-MM, YYYY, or MM.")
    return { 0: [None, None]
           , 2: [None, arg]
           , 4: [arg, None]
           , 7: arg.split('-')
           , 10: arg.split('-')[:2]
            }[len(arg)]


def list_datfiles(start=None, end=None, root='.'):
    """Given two (year, month) tuples, return a list of ['-f', filepath].

    Raises SystemExit if we don't have a datfile for a month in the
    range specified. May mutate start and/or end.

    """
    start = start or [None, None]
    end = end or start

    years = []
    months_by_year = defaultdict(list)
    for dirname in sorted(listdir(root)):
        if not dirname.startswith('FY'): continue
        for filename in sorted(listdir(path.join(root, dirname))):
            if re.match(r'\d\d\d\d-\d\d\.dat', filename) is None: continue
            year, month = filename[:-len('.dat')].split('-')
            years.append(year)
            months_by_year[year].append(month)

    if start[0] is None: start[0] = years[-1]
    if end[0] is None: end[0] = start[0]

    for year in start[0], end[0]:
        if year not in years:
            sys.exit("Sorry, we don't have any data for {}.".format(year))

    fiscal_years = set()
    months_to_load = []
    for year in years:
        if year < start[0]: continue
        elif year > end[0]: break

        months_for_year = months_by_year[year]

        def check(month):
            if month[1] not in months_for_year:
                sys.exit("Sorry, we don't have any data for {}-{}.".format(*month))

        if start[0] == year:
            if start[1] is None: start[1] = months_for_year[0]
            check(start)
        if end[0] == year:
            if end[1] is None: end[1] = months_for_year[-1]
            check(end)

        for month in months_for_year:
            if start[1] == year and month < start[1]: continue
            elif end[1] == year and month > end[1]: break

            fiscal_year = year if month < FISCAL_YEAR_STARTING_MONTH else unicode(int(year) + 1)
            fiscal_years.add(fiscal_year)
            months_to_load.append((fiscal_year, year, month))

    if end < start:
        sys.exit('Error: {}-{} comes before {}-{}.'.format(*(end + start)))

    declarations = ['-f ' + 'FY{}/declarations.dat'.format(fy) for fy in sorted(fiscal_years)]
    transactions = ['-f ' + 'FY{}/{}-{}.dat'.format(fy, y, m) for fy, y, m in months_to_load]
    return declarations + transactions


def income_statement():
    """Produce an income statement for one of three columns (operations, escrow, fee buffer)
    """
    column = path.basename(sys.argv[0]).rsplit('-', 1)[0]
    assert column in ('income', 'escrow', 'fee-buffer'), column
    title = column.replace('-', ' ').upper() + ' STATEMENT'
    filt = 'Operations' if column == 'income' else column.replace('-', ' ').title()

    cmd = [ 'ledger'
          , 'balance'
          , '"^Income:{}"'.format(filt)
          , '"^Expenses:{}"'.format(filt)
          , '--prepend-width=0' # this is here to satisfy ledger on Travis
          , '--limit "not (payee =~ /^Balance Sheet$/)"'
          , '--sort "account =~ /^Income.*/ ? 0 : '
          ,        '(account =~ /^Expense.*/ ? 1 : 2))"'
           ]
    cmd += sys.argv[1:]

    start, end = parse(sys.argv[1:])
    cmd += list_datfiles(start, end)

    print()
    print(title.center(42))
    if start == end:
        print("for {}, {}".format(calendar.month_name[int(end[1])], end[0]).center(42))
    elif start[0] == end[0]:
        print("for {} through {}, {}".format( calendar.month_name[int(start[1])]
                                            , calendar.month_name[int(end[1])]
                                            , end[0]).center(42)
                                             )
    else:
        print("for {}, {} through {}, {}".format( calendar.month_name[int(start[1])]
                                                , start[0]
                                                , calendar.month_name[int(end[1])]
                                                , end[0]
                                                 ).center(42))
    print()
    report(cmd)


def in_root(func):
    """This is a decorator to run a function in the repo root.
    """
    def wrapped(*a, **kw):
        old_cwd = getcwd()
        try:
            new_root = path.realpath(path.join(path.dirname(__file__), '..'))
            chdir(new_root)
            func(*a, **kw)
        finally:
            chdir(old_cwd)
    return wrapped


@in_root
def report(cmd):
    cmd.append('--pedantic')
    retcode = subprocess.call(' '.join(cmd), shell=True)
    if retcode != 0:
        raise SystemExit(retcode)
