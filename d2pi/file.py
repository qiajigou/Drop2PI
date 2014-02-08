# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from downloader import download


class File(object):

    def __repr__(self):
        return '<Dropbox File %s>' % self.path

    def __init__(self, size, rev, thumb_exists, bytes,
                 modified, mime_type, path, is_dir, icon, root,
                 client_mtime, revision):
        self.size = size
        self.rev = rev
        self.thumb_exists = thumb_exists
        self.bytes = bytes
        self.modified = datetime.strptime(modified,
                                          '%a, %d %b %Y %H:%M:%S +0000')
        self.mime_type = mime_type
        self.path = path
        self.is_dir = is_dir
        self.icon = icon
        self.root = root
        self.client_mtime = datetime.strptime(client_mtime,
                                              '%a, %d %b %Y %H:%M:%S +0000')
        self.revision = revision

    @property
    def save_to_dir(self):
        from config import PATH_TO_WATCH
        return '%s%s' % (PATH_TO_WATCH, self.path)

    def save(self):
        return download(self.path, self.save_to_dir)

    def is_exists(self):
        try:
            with open(self.save_to_dir):
                return True
        except:
            return False

    @property
    def last_modified(self):
        if not self.is_exists():
            return
        (mode, ino, dev, nlink, uid, gid, size,
         atime, mtime, ctime) = os.stat(self.save_to_dir)
        t = time.ctime(mtime)
        return datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
