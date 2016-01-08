"""This is a library to support Gratipay's financial reporting.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re
import sys
from os import path


root = path.realpath(path.join(path.dirname(__file__), '..'))


def parse(arg):
    """Given a command-line argument, return a (year, month) tuple.

    Raises SystemExit if the argument is in a bad format.

    """
    patterns = (r'^\d\d\d\d-\d\d$', r'^\d\d\d\d$', r'^\d\d$')
    if arg and not any([re.match(p, arg) for p in patterns]):
        sys.exit("Bad argument, must be YYYY-MM, YYYY, or MM.")
    return { 0: [None, None]
           , 2: [None, arg]
           , 4: [arg, None]
           , 7: arg.split('-')
            }[len(arg)]


def list_datfiles(start, end):
    """Given two (year, month) tuples, yield filepaths.

    Raises SystemExit if we don't have a datfile for a month in the
    range specified.

    """
    years = [y for y in sorted(os.listdir(root)) if y.isdigit()]
    if start[0] is None: start[0] = years[-1]
    if end[0] is None: end[0] = start[0]

    for year in start[0], end[0]:
        if year not in years:
            sys.exit("Sorry, we don't have the year {}.".format(year))

    filtered = []
    for year in years:
        if year < start[0]: continue
        elif year > end[0]: break

        months = [f[:2] for f in sorted(os.listdir(path.join(root, year))) if f.endswith('.dat')]

        if start[0] == year:
            if start[1] is None: start[1] = months[0]
            if start[1] not in months:
                sys.exit("Sorry, we don't have the month {}-{}.".format(*start))
        if end[0] == year:
            if end[1] is None: end[1] = months[-1]
            if end[1] not in months:
                sys.exit("Sorry, we don't have the month {}-{}.".format(*end))

        for month in months:
            if month < start[1]: continue
            elif month > end[1]: break

            filtered.append('{}/{}.dat'.format(year, month))

    return filtered
