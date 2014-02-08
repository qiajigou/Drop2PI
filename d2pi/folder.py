# -*- coding: utf-8 -*-

import os

from config import config


class Folder(object):

    def __repr__(self):
        return '<Dropbox Folder %s>' % self.path

    def __init__(self, hash, thumb_exists, bytes,
                 path, is_dir, icon, root, contents):
        self.hash = hash
        self.thumb_exists = thumb_exists
        self.bytes = bytes
        self.path = path
        self.is_dir = is_dir
        self.icon = icon
        self.root = root
        self.contents = contents or []

    @property
    def files(self):
        from file import File
        rs = self._get_contents(need_dir=False)
        return [File(*r) for r in rs]

    @property
    def dirs(self):
        rs = self._get_contents(need_dir=True)
        fs = [Folder(*r) for r in rs]
        return [Folder.get_by_path(f.path) for f in fs]

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
                rs.append((hash, thumb_exists, bytes,
                           path, is_dir, icon, root, contents))
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
                client_mtime = c.get('client_mtime')
                revision = c.get('revision')
                rs.append((size, rev, thumb_exists, bytes,
                           modified, mime_type, path, is_dir,
                           icon, root, client_mtime, revision))
        return rs

    @classmethod
    def get_by_path(cls, path):
        client = config.client
        md = client.metadata(path)
        hash = md.get('hash')
        thumb_exists = md.get('thumb_exists')
        bytes = md.get('bytes')
        path = md.get('path')
        is_dir = md.get('is_dir')
        icon = md.get('icon')
        root = md.get('root')
        contents = md.get('contents')
        return cls(hash, thumb_exists, bytes,
                   path, is_dir, icon, root, contents)

    @property
    def save_to_dir(self):
        from config import PATH_TO_WATCH
        return '%s%s' % (PATH_TO_WATCH, self.path)

    def save(self):
        if self.is_exists():
            print '%s exists' % self.save_to_dir
            return
        print 'mkdir %s' % self.save_to_dir
        os.makedirs(self.save_to_dir)
        f = Folder.get_by_path(self.path)
        self = f

    def is_exists(self):
        if os.path.exists(self.save_to_dir):
            return True
        return False
