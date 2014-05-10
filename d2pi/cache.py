# -*- coding: utf-8 -*-
# a simple cache in mm

if not 'd2_dir_cache' in globals():
    global d2_dir_cache

if not 'd2_files_list' in globals():
    global d2_files_list


class _D2DirDictCache(dict):

    def save(self):
        pass


class _D2FilesListCache(object):

    _l = []

    def __repr__(self):
        return str(self._l)

    def __nonzero__(self):
        if self._l:
            return True
        return False

    # for python 3
    __bool__ = __nonzero__

    def set(self, val):
        self._l.append(val)

    def delete(self, val):
        try:
            self._l.remove(val)
            return True
        except:
            return False

    def delete_by_prefix(self, prefix):
        _r = []
        for i in self._l:
            if not i.startswith(prefix):
                _r.append(i)
        self._l = _r

    def has_value(self, val):
        if self._l.count(val):
            return True
        return False

    def clear(self):
        self._l = []

d2_files_list = _D2FilesListCache()
d2_dir_cache = _D2DirDictCache()
