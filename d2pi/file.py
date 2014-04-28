# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from client import Client


class File(object):

    def __repr__(self):
        return '<Dropbox File %s>' % self.path

    def __init__(self, size, rev, thumb_exists, bytes,
                 modified, mime_type, path, is_dir, icon, root,
                 client_mtime, revision, is_deleted):
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
        self.is_deleted = is_deleted

    @property
    def save_to_dir(self):
        from config import config
        return '%s%s' % (config.path_to_watch, self.path)

    def save(self):
        from config import config
        if self.bytes > config.download_max:
            # if file larger than 2M
            # do not download big file
            # try other way
            try:
                Client.prepare_download_bigfile(self.path)
            except:
                pass
            return
        return Client.download(self.path, self.save_to_dir)

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
