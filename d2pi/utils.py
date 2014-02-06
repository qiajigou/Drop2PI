# -*- coding: utf-8 -*-


def parse_file_dir(file_path):
    '''
    input:  /some1/some2/filename.txt
    return: filename.txt
    '''
    f = file_path.split('/')
    return f[-1]


def md5_for_file(f, block_size=2 ** 20):
    import hashlib
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()
