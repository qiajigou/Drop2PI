# -*- coding: utf-8 -*-
import os
import sys
import socket
from config import config
from utils import parse_file_dir


def upload(file_name, as_file_name):
    print "uploading %s to %s" % (file_name, as_file_name)
    socket.setdefaulttimeout(10)
    client = config.client
    try:
        if not client:
            return
        with open(file_name, 'r') as f:
            client.put_file(as_file_name, f, overwrite=True)
            print 'uploaded'
    except Exception, e:
        print 'Error %s' % e


def create_folder(path):
    print 'create folder %s' % path
    socket.setdefaulttimeout(10)
    client = config.client
    try:
        client.file_create_folder(path)
    except Exception, e:
        print 'Error %s' % e


def delete(path):
    print 'delete %s' % path
    socket.setdefaulttimeout(10)
    client = config.client
    try:
        client.file_delete(path)
    except Exception, e:
        print 'Error %s' % e
    try:
        path = config.path_to_watch + path
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    except:
        pass


def move(path, to_path):
    print 'move %s to %s' % (path, to_path)
    socket.setdefaulttimeout(10)
    client = config.client
    try:
        client.file_move(path, to_path)
    except Exception, e:
        print 'Error %s' % e


def check_dir_deleted(path=''):
    socket.setdefaulttimeout(10)
    path = path or config.path_to_watch

    for l in os.listdir(path):
        tmp_path = path + '/' + l
        if os.path.isdir(tmp_path):
            check_dir_deleted(tmp_path)
        _check_delete(tmp_path)

    _check_delete(path)


def _check_delete(path):
    if not config.delete_local_file:
        return
    if path == config.path_to_watch:
        return
    path = path.replace(config.path_to_watch, '')
    client = config.client
    try:
        m = client.metadata(path)
        if m.get('is_deleted'):
            delete(path)
    except:
        pass

if __name__ == "__main__":
    args = sys.argv
    args = args[1:]
    file_name, as_file_name = '', ''
    if len(args) == 1:
        file_name = args[0]
        as_file_name = parse_file_dir(file_name)
    elif len(args) == 2:
        file_name, as_file_name = args
    try:
        upload(file_name, as_file_name)
    except Exception, e:
        print 'Try to use this tools as'
        print 'dropbox-uploader.py filename asfilename'
        print 'Error: %s' % e
