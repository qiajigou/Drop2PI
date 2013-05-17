# -*- coding: utf-8 -*-
import sys

from utils import get_client, parse_file_dir

def upload(file_name, as_file_name):
    print "Uploading %s to %s" % (file_name, as_file_name)
    r = 'No Result'
    try:
        f = open(file_name)
        client = get_client()
        if not client:
            return
        client.put_file(as_file_name, f, overwrite=True)
    except Exception, e:
        print 'Error %s' % e
        f.close()

def delete(path):
    client = get_client()
    try:
        client.file_delete(path)
    except Exception, e:
        print 'Error %s' % e

def move(path, to_path):
    client = get_client()
    try:
        client.file_move(path, to_path)
    except Exception, e:
        print 'Error %s' % e

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
