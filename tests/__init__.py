# -*- coding: utf-8 -*-

from sys import version_info

__all__ = ['unittest']

if version_info < (2, 7):
    try:
        import unittest2 as unittest
    except:
        import unittest
else:
    import unittest

from d2pi.cache import d2_files_list


class TestBase(unittest.TestCase):
    def setUp(self):
        d2_files_list.clear()

    def tearDown(self):
        d2_files_list.clear()
