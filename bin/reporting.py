"""This is a library to support Gratipay's financial reporting.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import subprocess
import re
import sys
from os import chdir, getcwd, listdir, path


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

    years = [y for y in sorted(listdir(root)) if y.isdigit()]
    if start[0] is None: start[0] = years[-1]
    if end[0] is None: end[0] = start[0]

    for year in start[0], end[0]:
        if year not in years:
            sys.exit("Sorry, we don't have any data for {}.".format(year))

    filtered = []
    for year in years:
        if year < start[0]: continue
        elif year > end[0]: break

        months = [f[:2] for f in sorted(listdir(path.join(root, year))) if f.endswith('.dat')]

        def check(month):
            if month[1] not in months:
                sys.exit("Sorry, we don't have any data for {}-{}.".format(*month))

        if start[0] == year:
            if start[1] is None: start[1] = months[0]
            check(start)
        if end[0] == year:
            if end[1] is None: end[1] = months[-1]
            check(end)

        for month in months:
            if start[1] == year and month < start[1]: continue
            elif end[1] == year and month > end[1]: break

            filtered.append('{}/{}.dat'.format(year, month))

    if end < start:
        sys.exit('Error: {}-{} comes before {}-{}.'.format(*(end + start)))

    return ['-f ' + f for f in filtered]


def report(cmd):
    cwd = getcwd()
    try:
        chdir(path.realpath(path.join(path.dirname(__file__), '..')))
        cmd += ['-f', 'declarations.dat']
        retcode = subprocess.call(' '.join(cmd), shell=True)
        if retcode != 0:
            raise SystemExit(retcode)
    finally:
        chdir(cwd)
