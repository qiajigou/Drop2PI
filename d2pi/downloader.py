# -*- coding: utf-8 -*-
import sys

from utils import get_client, parse_file_dir

def download(file_path, save_to_path):
    if '/' == save_to_path[-1]:
        save_to_path = save_to_path[:-1]
    print 'Downloading %s and save to %s' % (file_path, save_to_path)
    client = get_client()
    if not client:
        return
    f, m = client.get_file_and_metadata(file_path)
    print 'Downloaded'
    d = f.read()
    f = open(save_to_path, 'w')
    f.write(d)
    f.close()

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
