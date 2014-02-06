# -*- coding: utf-8 -*-
import sys

import socket
from config import config
from utils import md5_for_file


def download(file_path, save_to_path):
    socket.setdefaulttimeout(10)
    if '/' == save_to_path[-1]:
        save_to_path = save_to_path[:-1]
    client = config.client
    if not client:
        return
    f, m = client.get_file_and_metadata(file_path)
    d = f.read()
    f_hash = ''
    try:
        with open(save_to_path) as f:
            f_hash = md5_for_file(f)
    except:
        pass
    try:
        f = open(save_to_path, 'rw')
        fd_hash = md5_for_file(f)
        if f_hash == fd_hash:
            return False
    except:
        f.close()
    print 'downloading %s and save to %s' % (file_path, save_to_path)
    f = open(save_to_path, 'w')
    f.write(d)
    f.close()
    print 'downloaded'
    return True

if __name__ == '__main__':
    args = sys.argv
    args = args[1:]
    file_path, as_to_path = '', ''
    if len(args) == 1:
        file_path = args[0]
        save_to_path = './'
    elif len(args) == 2:
        file_path, save_to_path = args
    try:
        download(file_path, save_to_path)
    except Exception, e:
        print 'Error %s' % e
