# -*- coding: utf-8 -*-

import os
import time
import sys
from folder import Folder
from config import config
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
    if not os.path.exists(config.path_to_watch):
        print 'mkdir %s' % config.path_to_watch
        os.makedirs(config.path_to_watch)


def clean():
    return
    if os.path.exists(config.path_to_watch):
        print 'rm -rf %s' % config.path_to_watch
        os.system('rm -rf %s' % config.path_to_watch)


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
            dropbox_path = path.replace(config.path_to_watch, '')
            print 'file %s changed, updating...' % dropbox_path
            upload(path, dropbox_path)
    except:
        pass


def sync_upload_create(event):
    try:
        path = event.src_path
        dropbox_path = path.replace(config.path_to_watch, '')
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
        dropbox_path = path.replace(config.path_to_watch, '')
        print 'file %s deleted, updating...' % dropbox_path
        delete(dropbox_path)
    except:
        pass


def sync_upload_move(event):
    try:
        print dir(event)
        dropbox_to_path = event.dest_path.replace(config.path_to_watch, '')
        dropbox_from_path = event.src_path.replace(config.path_to_watch, '')
        print 'file moved from %s to %s, updating...' % (dropbox_from_path,
                                                         dropbox_to_path)
        move(dropbox_from_path, dropbox_to_path)
    except:
        pass


def sync_any_event(event):
    '''
    any event on a dir
    this method will be called
    '''


def go_watch():
    print 'Start watching %s' % config.path_to_watch
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, config.path_to_watch, recursive=True)
    observer.start()
    event_handler.on_modified = sync_upload
    event_handler.on_deleted = sync_upload_delete
    event_handler.on_created = sync_upload_create
    event_handler.on_moved = sync_upload_move
    event_handler.on_any_event = sync_any_event
    time_loop = 1
    try:
        while True:
            time.sleep(1)
            time_loop += 1
            if not time_loop % config.auto_aync_time and config.auto_check:
                print 'Auto sync every %s second' % config.auto_aync_time
                if not observer.event_queue.unfinished_tasks:
                    sync_download()
                    check_dir_deleted()
                print 'Auto check downloaded file or folder'
                check_dir_deleted()
    except KeyboardInterrupt:
        print 'End watching.'
        observer.stop()
    observer.join()


def _start():
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

if __name__ == '__main__':
    print '******************************************'
    print '        THANKS FOR USING DROP2PI'
    print '         GUOJING soundbbg@gmail'
    print '           thanks to bettylwx'
    print '******************************************'
    print 'Starting...'
    if not config.is_useable():
        print 'ERROR: Please set config of %s' % config.filename
    else:
        _start()
