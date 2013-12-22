# -*- coding: utf-8 -*-

import os
import time
import sys
from folder import Folder
from config import PATH_TO_WATCH, AUTO_SYNC_TIME
from uploader import upload, delete, move, create_folder, check_dir_deleted
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def sync(folder):
    for f in folder.files:
        f.save()
    if not folder.dirs:
        return
    for d in folder.dirs:
        d.save()
        sync(d)


def init():
    if not os.path.exists(PATH_TO_WATCH):
        print 'mkdir %s' % PATH_TO_WATCH
        os.makedirs(PATH_TO_WATCH)


def clean():
    return
    if os.path.exists(PATH_TO_WATCH):
        print 'rm -rf %s' % PATH_TO_WATCH
        os.system('rm -rf %s' % PATH_TO_WATCH)


def sync_download():
    try:
        init()
        f = Folder.get_by_path('/')
        sync(f)
    except:
        pass


def sync_upload(event):
    try:
        if not event.is_directory:
            path = event.src_path
            dropbox_path = path.replace(PATH_TO_WATCH, '')
            print 'file %s changed, updating...' % dropbox_path
            upload(path, dropbox_path)
    except:
        pass


def sync_upload_create(event):
    try:
        path = event.src_path
        dropbox_path = path.replace(PATH_TO_WATCH, '')
        print 'file %s created, updating...' % dropbox_path
        if event.is_directory:
            create_folder(dropbox_path)
        else:
            upload(path, dropbox_path)
    except:
        pass


def sync_upload_delete(event):
    try:
        path = event.src_path
        dropbox_path = path.replace(PATH_TO_WATCH, '')
        print 'file %s deleted, updating...' % dropbox_path
        delete(dropbox_path)
    except:
        pass


def sync_upload_move(event):
    try:
        print dir(event)
        dropbox_to_path = event.dest_path.replace(PATH_TO_WATCH, '')
        dropbox_from_path = event.src_path.replace(PATH_TO_WATCH, '')
        print 'file moved from %s to %s, updating...' % (dropbox_from_path,
                                                         dropbox_to_path)
        move(dropbox_from_path, dropbox_to_path)
    except:
        pass


def go_watch():
    try:
        print 'Start watching %s' % PATH_TO_WATCH
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, PATH_TO_WATCH, recursive=True)
        observer.start()
        event_handler.on_modified = sync_upload
        event_handler.on_deleted = sync_upload_delete
        event_handler.on_created = sync_upload_create
        event_handler.on_moved = sync_upload_move
        time_loop = 1
        try:
            while True:
                time.sleep(1)
                time_loop += 1
                if not time_loop % AUTO_SYNC_TIME:
                    print 'Auto sync every %s second' % AUTO_SYNC_TIME
                    if not observer.event_queue.unfinished_tasks:
                        sync_download()
                        check_dir_deleted()
                    print 'Auto check downloaded file or folder'
                    check_dir_deleted()
        except KeyboardInterrupt:
            print 'End watching.'
            observer.stop()
        observer.join()
    except Exception, e:
        print '*' * 10
        print e
        print '*' * 10
        return

if __name__ == '__main__':
    print '******************************************'
    print '        THANKS FOR USING DROP2PI'
    print '         GUOJING soundbbg@gmail'
    print '           thanks to bettylwx'
    print '******************************************'
    print 'Starting...'
    init()
    args = sys.argv
    args = args[1:]
    watch = True
    download = True
    if args:
        if '-c' == args[0]:
            clean()
        if '-e' == args[0]:
            watch = False
        if '-r' == args[0]:
            download = False
    if download:
        print 'Start download files...'
        sync_download()
        check_dir_deleted()
        print 'Sync server end.'
    print 'Start end.'
    if watch:
        while True:
            go_watch()
