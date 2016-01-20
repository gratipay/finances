#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from os import path, chdir

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

OLD, NEW = sys.argv[1:3]


'''
    Assets:Escrow:Samurai                                           $     3.30
'''

chdir(reporting.root)
for filename in reporting.list_datfiles():
    with open(filename, 'r') as fp:
        contents = fp.read()
    for tmpl in ("    {:<64}$", "    {:<63}-$", "    {}\n"):
        old = tmpl.format(OLD)
        new = tmpl.format(NEW)
        print(old)
        print(new)
        contents = contents.replace(old, new)
    with open(filename, 'w+') as fp:
        fp.write(contents)
