# -*- coding: utf-8 -*-

import os
import time
import logging

from folder import Folder
from config import config
from client import client
from utils import get_logger

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logger = get_logger(config.path_to_watch)


class Watcher(object):
    '''
    This is Watcher Object of DROP2PI
    '''
    observer = None

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
        if not folder.dirs:
            return
        for d in folder.dirs:
            d.save()
            self.sync(d)

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
        try:
            self.init()
            f = Folder.get_by_path('/')
            self.sync(f)
        except:
            pass

    def sync_upload(self, event):
        '''
        upload event
        '''
        try:
            if not event.is_directory:
                path = event.src_path
                dropbox_path = path.replace(config.path_to_watch, '')
                logger.info('file %s changed, updating...' % dropbox_path)
                client.upload(path, dropbox_path)
        except:
            pass

    def sync_create(self, event):
        '''
        create event
        '''
        try:
            path = event.src_path
            dropbox_path = path.replace(config.path_to_watch, '')
            logger.info('file %s created, updating...' % dropbox_path)
            if event.is_directory:
                client.create_folder(dropbox_path)
            else:
                client.upload(path, dropbox_path)
        except:
            pass

    def sync_delete(self, event):
        '''
        delete event
        '''
        try:
            path = event.src_path
            dropbox_path = path.replace(config.path_to_watch, '')
            logger.info('file %s deleted, updating...' % dropbox_path)
            client.delete(dropbox_path)
        except:
            pass

    def sync_move(self, event):
        '''
        move event
        '''
        try:
            dropbox_to_path = event.dest_path.replace(config.path_to_watch,
                                                      '')
            dropbox_from_path = event.src_path.replace(config.path_to_watch,
                                                       '')
            logger.info('file moved from %s to %s, updating...' %
                        (dropbox_from_path, dropbox_to_path))
            client.move(dropbox_from_path, dropbox_to_path)
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

    def run(self):
        '''
        run watcher
        '''
        observer = self.create_observer()
        observer.start()

        time_loop = 1
        try:
            while True:
                time.sleep(1)
                time_loop += 1
                if not time_loop % config.auto_aync_time and config.auto_check:
                    logger.info('Auto sync every %s second' %
                                config.auto_aync_time)
                    if not observer.event_queue.unfinished_tasks:
                        self.sync_download()
                        client.check_dir_deleted()
                    logger.info('Auto check downloaded file or folder')
                    client.check_dir_deleted()
        except KeyboardInterrupt:
            logger.info('End watching.')
            observer.stop()
        observer.join()
