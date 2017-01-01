"""This is a library to support Gratipay's financial reporting.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from os import chdir, getcwd, path


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

