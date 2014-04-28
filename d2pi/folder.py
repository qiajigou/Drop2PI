# -*- coding: utf-8 -*-

import os

from config import config
from cache import d2_dir_cache

from utils import get_logger
logger = get_logger(config.path_to_watch)

# pylint: disable=E1103


class Folder(object):

    def __repr__(self):
        return '<Dropbox Folder %s>' % self.path

    def __init__(self, hash, thumb_exists, bytes,
                 path, is_dir, icon, root, contents,
                 is_deleted):
        self.hash = hash
        self.thumb_exists = thumb_exists
        self.bytes = bytes
        self.path = path
        self.is_dir = is_dir
        self.icon = icon
        self.root = root
        self.is_deleted = is_deleted
        self.contents = contents or []

    @property
    def _files(self):
        from file import File
        rs = self._get_contents(need_dir=False)
        return [File(*r) for r in rs]

    @property
    def files(self):
        return [f for f in self._files if not f.is_deleted]

    @property
    def deleted_files(self):
        return [f for f in self._files if f.is_deleted]

    @property
    def _dirs(self):
        rs = self._get_contents(need_dir=True)
        fs = [Folder(*r) for r in rs]
        return [Folder.get_by_path(f.path) for f in fs]

    @property
    def dirs(self):
        return [d for d in self._dirs if not d.is_deleted]

    @property
    def deleted_dirs(self):
        return [d for d in self._dirs if d.is_deleted]

    def _get_contents(self, need_dir=False):
        rs = []
        for c in self.contents:
            if need_dir:
                if not c.get('is_dir'):
                    continue
                hash = c.get('hash')
                thumb_exists = c.get('thumb_exists')
                bytes = c.get('bytes')
                path = c.get('path')
                is_dir = c.get('is_dir')
                icon = c.get('icon')
                root = c.get('root')
                contents = c.get('contents')
                is_deleted = c.get('is_deleted', False)
                rs.append((hash, thumb_exists, bytes,
                           path, is_dir, icon, root, contents,
                           is_deleted))
            else:
                if c.get('is_dir'):
                    continue
                size = c.get('size')
                rev = c.get('rev')
                thumb_exists = c.get('thumb_exists')
                bytes = c.get('bytes')
                modified = c.get('modified')
                mime_type = c.get('mime_type')
                path = c.get('path')
                is_dir = c.get('is_dir')
                icon = c.get('icon')
                root = c.get('root')
                is_deleted = c.get('is_deleted', False)
                client_mtime = c.get('client_mtime')
                revision = c.get('revision')
                rs.append((size, rev, thumb_exists, bytes,
                           modified, mime_type, path, is_dir,
                           icon, root, client_mtime, revision,
                           is_deleted))
        return rs

    @classmethod
    def get_by_path(cls, path):
        path = str(path)
        _cache = d2_dir_cache.get(path, None)
        _hash = None
        try:
            _hash = _cache.hash if _cache else None
            if _cache and _cache.hash:
                logger.info('cache hit for %s' % path)
        except:
            _hash = None
        client = config.client
        try:
            md = client.metadata(path, hash=_hash, include_deleted=True)
            hash = md.get('hash')
            thumb_exists = md.get('thumb_exists')
            bytes = md.get('bytes')
            path = md.get('path')
            is_dir = md.get('is_dir')
            icon = md.get('icon')
            root = md.get('root')
            contents = md.get('contents')
            is_deleted = md.get('is_deleted', False)
            logger.info('set cache for %s' % path)
            r = cls(hash, thumb_exists, bytes,
                    path, is_dir, icon, root, contents,
                    is_deleted)
            d2_dir_cache[path] = r
            return r
        except:
            # get metadata wish hash
            # if no change dropbox will raise exception
            logger.info('return cache for %s' % path)
            return _cache if _cache else None

    @property
    def save_to_dir(self):
        from config import config
        return '%s%s' % (config.path_to_watch, self.path)

    def save(self):
        if self.is_exists():
            print('%s exists' % self.save_to_dir)
            return
        print('mkdir %s' % self.save_to_dir)
        os.makedirs(self.save_to_dir)
        f = Folder.get_by_path(self.path)
        self = f

    def is_exists(self):
        if os.path.exists(self.save_to_dir):
            return True
        return False

# pylint enable=E1103
