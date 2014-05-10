# -*- coding: utf-8 -*-

from tests import TestBase
from d2pi.cache import d2_files_list


class SimpleCacheTest(TestBase):
    def test_set_simple_cache(self):
        key = 'test'
        self.assertFalse(d2_files_list)
        d2_files_list.set(key)
        self.assertTrue(d2_files_list.has_value(key))
        d2_files_list.delete(key)
        self.assertFalse(d2_files_list.has_value(key))

    def test_simple_cache_has_value(self):
        key = 'test'
        self.assertFalse(d2_files_list)
        d2_files_list.set(key)
        self.assertTrue(d2_files_list.has_value(key))

    def test_delete_cache_by_prefix(self):
        key = ['test1', 'test2', 'notest']
        for i in key:
            d2_files_list.set(i)
        d2_files_list.delete_by_prefix('test')
        self.assertTrue(d2_files_list)
        self.assertFalse(d2_files_list.has_value('test1'))
        self.assertFalse(d2_files_list.has_value('test2'))
        self.assertTrue(d2_files_list.has_value('notest'))
