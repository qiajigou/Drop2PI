# -*- coding: utf-8 -*-
import os
import sys
import socket
from config import PATH_TO_WATCH
from utils import get_client, parse_file_dir, md5_for_file

def upload(file_name, as_file_name):
    print "uploading %s to %s" % (file_name, as_file_name)
    socket.setdefaulttimeout(10)
    try:
        client = get_client()
        if not client:
            return
        f = open(file_name)
        client.put_file(as_file_name, f, overwrite=True)
        print 'uploaded'
    except Exception, e:
        print 'Error %s' % e
        f.close()

def create_folder(path):
    print 'create folder %s' % path
    socket.setdefaulttimeout(10)
    client = get_client()
    try:
        client.file_create_folder(path)
    except Exception, e:
        print 'Error %s' % e

def delete(path):
    print 'delete %s' % path
    socket.setdefaulttimeout(10)
    client = get_client()
    try:
        client.file_delete(path)
    except Exception, e:
        print 'Error %s' % e
    try:
        path = PATH_TO_WATCH + path
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    except:
        pass

def move(path, to_path):
    print 'move %s to %s' % (path, to_path)
    socket.setdefaulttimeout(10)
    client = get_client()
    try:
        client.file_move(path, to_path)
    except Exception, e:
        print 'Error %s' % e

def check_dir_deleted(path=''):
    socket.setdefaulttimeout(10)
    path = path or PATH_TO_WATCH

    for l in os.listdir(path):
        tmp_path = path + '/' + l
        if os.path.isdir(tmp_path):
            check_dir_deleted(tmp_path)
        _check_delete(tmp_path)

    _check_delete(path)

def _check_delete(path):
    client = get_client()
    if path == PATH_TO_WATCH:
        return
    path = path.replace(PATH_TO_WATCH, '')
    try:
        m = client.metadata(path)
        if m.get('is_deleted'):
            delete(path)
    except:
        try:
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
