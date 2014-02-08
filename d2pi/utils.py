# -*- coding: utf-8 -*-

import logging


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


def get_logger(path=None):
    if not getattr(get_logger, '_logger', None):
        logger = logging.getLogger('d2pi')
        logger.setLevel(logging.INFO)
        log_file = 'd2pi.log'
        fh = logging.FileHandler(log_file)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(name)s %(asctime)s %(levelname)-s %(message)s',
            '%Y:%m:%d %H:%M:%S',)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        get_logger._logger = logger
    return get_logger._logger
