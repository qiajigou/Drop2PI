# -*- coding: utf-8 -*-
import sys, os, time
from folder import Folder
from config import PATH_TO_WATCH
from uploader import upload, delete, move
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
    if os.path.exists(PATH_TO_WATCH):
        print 'rm -rf %s' % PATH_TO_WATCH
        os.system('rm -rf %s' % PATH_TO_WATCH)

def sync_download():
    init()
    f = Folder.get_by_path('/')
    sync(f)

def sync_upload(event):
    if not event.is_directory:
        path = event.src_path
        dropbox_path = path.replace(PATH_TO_WATCH, '')
        print 'file %s changed, uploading...' % dropbox_path
        upload(path, dropbox_path)
        sync_download()

def sync_upload_create(event):
    path = event.src_path
    dropbox_path = path.replace(PATH_TO_WATCH, '')
    print 'file %s created, uploading...' % dropbox_path
    upload(path, dropbox_path)
    sync_download()

def sync_upload_delete(event):
    path = event.src_path
    dropbox_path = path.replace(PATH_TO_WATCH, '')
    print 'file %s deleted, uploading...' % dropbox_path
    delete(dropbox_path)
    sync_download()

def sync_upload_move(event):
    print dir(event)
    dropbox_to_path = event.dest_path.replace(PATH_TO_WATCH, '')
    dropbox_from_path = event.src_path.replace(PATH_TO_WATCH, '')
    print 'file moved from %s to %s, uploading...' % (dropbox_from_path,
            dropbox_to_path)
    move(dropbox_from_path, dropbox_to_path)
    sync_download()

if __name__ == '__main__':
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
        sync_download()
    if watch:
        print 'Start watching...'
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
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print 'End watching.'
            observer.stop()
        observer.join()
