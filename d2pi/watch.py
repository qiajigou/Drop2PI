# -*- coding: utf-8 -*-

import logging
import os
import time
from config import config

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from client import client
from eventq import EventQueue
from folder import Folder
from lock import (free_lock, free_upload_lock, get_lock, get_upload_lock,
                  set_lock, set_upload_lock)
from utils import get_logger

logger = get_logger(config.path_to_watch)
queue = EventQueue(100)


class Watcher(object):
    '''
    This is Watcher Object of DROP2PI
    '''
    observer = None
    can_upload = True
    can_download = True
    can_delete = True

    def __repr__(self):
        return '<Watcher>'

    def init(self):
        '''
        init path of watching dir
        '''
        if not os.path.exists(config.path_to_watch):
            logger.info('mkdir %s' % config.path_to_watch)
            os.makedirs(config.path_to_watch)

    def sync(self, folder):
        '''
        sync files
        '''
        for f in folder.files:
            f.save()
        for d in folder.dirs:
            d.save()
            self.sync(d)
        if not self.can_delete:
            return
        if not config.delete_local_file:
            return
        for f in folder.deleted_files:
            if f.path in ('/', config.path_to_watch):
                continue
            _path = config.path_to_watch + f.path
            if os.path.exists(_path):
                logger.info('rm %s' % _path)
                os.system('rm %s' % _path)
        for d in folder.deleted_dirs:
            if f.path in ('/', config.path_to_watch):
                continue
            _path = config.path_to_watch + d.path
            if os.path.exists(_path):
                logger.info('rm -rf %s' % _path)
                os.system('rm -rf %s' % _path)

    def clean(self):
        '''
        remove all files in watching dir
        '''
        if os.path.exists(config.path_to_watch):
            logger.info('rm -rf %s' % config.path_to_watch)
            os.system('rm -rf %s' % config.path_to_watch)

    def sync_download(self):
        '''
        start to download all files in watching dir
        '''
        if not self.can_download:
            logger.info('Download mode is disabled, will not download.')
            return
        if get_lock():
            return
        try:
            set_lock()
            self.init()
            f = Folder.get_by_path('/')
            self.sync(f)
            free_lock()
        except:
            pass

    def sync_upload(self, event):
        '''
        upload event
        '''
        if not self.can_upload:
            logger.info('Upload mode is disabled, will not upload.')
            return
        if get_upload_lock():
            logger.info('Uploading lock, will not upload this time')
            return
        try:
            set_lock()
            if not event.is_directory:
                path = event.src_path
                dropbox_path = path.replace(config.path_to_watch, '')
                logger.info('file %s changed, updating...' % dropbox_path)
                client.upload(path, dropbox_path)
            free_lock()
        except:
            pass

    def sync_create(self, event):
        '''
        create event
        '''
        if not self.can_upload:
            logger.info('Upload mode is disabled, will not upload.')
            return
        if get_upload_lock():
            logger.info('Creating lock, will not upload this time')
            return
        try:
            set_lock()
            path = event.src_path
            dropbox_path = path.replace(config.path_to_watch, '')
            logger.info('file %s created, updating...' % dropbox_path)
            if event.is_directory:
                client.create_folder(dropbox_path)
            else:
                client.upload(path, dropbox_path)
            free_lock()
        except:
            pass

    def sync_delete(self, event):
        '''
        delete event
        '''
        if not self.can_delete:
            # disable delete files to server is safe mode
            logger.info('Delete mode is disabled, will not delete.')
            return
        try:
            set_lock()
            path = event.src_path
            dropbox_path = path.replace(config.path_to_watch, '')
            logger.info('file %s deleted, updating...' % dropbox_path)
            client.delete(dropbox_path)
            free_lock()
        except:
            pass

    def sync_move(self, event):
        '''
        move event
        '''
        try:
            set_lock()
            dropbox_to_path = event.dest_path.replace(config.path_to_watch,
                                                      '')
            dropbox_from_path = event.src_path.replace(config.path_to_watch,
                                                       '')
            logger.info('file moved from %s to %s, updating...' %
                        (dropbox_from_path, dropbox_to_path))
            client.move(dropbox_from_path, dropbox_to_path)
            free_lock()
        except:
            pass

    def sync_any_event(self, event):
        '''
        any event on a dir
        this method will be called
        '''

    def create_observer(self):
        '''
        create a watchdog observer
        '''
        logger.info('Start watching %s' % config.path_to_watch)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        observer = Observer()
        self.observer = observer
        event_handler.on_modified = self.sync_upload
        event_handler.on_deleted = self.sync_delete
        event_handler.on_created = self.sync_create
        event_handler.on_moved = self.sync_move
        event_handler.on_any_event = self.sync_any_event
        observer.schedule(event_handler, config.path_to_watch, recursive=True)
        return observer

    def run(self, upload=True, download=True, delete=True):
        '''
        run watcher
        if upload is True, new files will be upload
        if upload is False, it's download only mode.
        ----
        if download is True, files will be downloaded
        else files will not download.
        ----
        if delete is True, delete local file will delete remote
        else is safe mode, for download only mode.

        NOTE: by default, all options are True and you don't need to care
        if you use this tool for only download and don't want others
        remove your file, you can set delete to False.
        '''
        self.can_upload = upload
        self.can_download = download
        self.can_delete = delete
        if not upload:
            self.can_delete = False

        observer = self.create_observer()
        observer.start()

        time_loop = 1
        try:
            while True:
                time.sleep(1)
                time_loop += 1
                if not time_loop % config.auto_aync_time and config.auto_check:
                    set_upload_lock()
                    if get_lock():
                        logger.info('Something is working, '
                                    'not download right now...')
                        free_upload_lock()
                        continue
                    logger.info('Auto sync every %s second' %
                                config.auto_aync_time)
                    self.sync_download()
                    # client.check_dir_deleted()
                    free_upload_lock()
                    queue.run()
        except KeyboardInterrupt:
            logger.info('End watching.')
            observer.stop()
        observer.join()
