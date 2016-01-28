#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from os import path

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting


@reporting.in_root
def rename():
    old_name, new_name = sys.argv[1:3]
    for dash_f in reporting.list_datfiles():
        filename = dash_f[len('-f '):]
        with open(filename, 'r') as fp:
            contents = fp.read()
        for tmpl in ("    {:<64}$", "    {:<63}-$"):
            old = tmpl.format(old_name)
            new = tmpl.format(new_name)
            contents = contents.replace(old, new)
        with open(filename, 'w+') as fp:
            fp.write(contents)

if __name__ == '__main__':
    rename()
