# -*- coding: utf-8 -*-
import os
import socket

from config import config
from utils import md5_for_file, get_logger

logger = get_logger(config.path_to_watch)


class Client(object):
    '''
    A simple interface of Dropbox Client
    '''
    @classmethod
    def upload(cls, file_name, as_file_name):
        '''
        upload file_name to as_file_name
        '''
        socket.setdefaulttimeout(10)
        client = config.client
        logger.info('upload file %s to %s' % (file_name,
                                              as_file_name))
        try:
            if not client:
                return
            with open(file_name, 'r') as f:
                client.put_file(as_file_name, f, overwrite=True)
            logger.info('uploaded')
        except Exception, e:
            logger.error(e)

    @classmethod
    def create_folder(cls, path):
        '''
        create folder
        '''
        logger.info('create folder %s' % path)
        socket.setdefaulttimeout(10)
        client = config.client
        try:
            client.file_create_folder(path)
        except Exception, e:
            logger.error(e)

    @classmethod
    def delete(cls, path):
        '''
        delete a path
        '''
        logger.info('delete %s' % path)
        socket.setdefaulttimeout(10)
        client = config.client
        try:
            client.file_delete(path)
        except Exception, e:
            logger.error('Error %s' % e)

    @classmethod
    def move(cls, path, to_path):
        '''
        move file from path to to_path
        '''
        logger.info('move %s to %s' % (path, to_path))
        socket.setdefaulttimeout(10)
        client = config.client
        try:
            client.file_move(path, to_path)
        except Exception, e:
            logger.error(e)

    @classmethod
    def download(cls, file_path, save_to_path):
        '''
        download file from server
        from file_path to save_to_path
        '''
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
        logger.info('downloading %s and save to %s' % (file_path,
                                                       save_to_path))
        f = open(save_to_path, 'w')
        f.write(d)
        f.close()
        logger.info('downloaded')
        return True

    @classmethod
    def check_dir_deleted(cls, path=''):
        '''
        check dir is is_deleted
        if is deleted in server
        local path should be deleted to
        but if config.delete_local_file is False
        this will not delete file
        '''
        socket.setdefaulttimeout(10)
        path = path or config.path_to_watch

        for l in os.listdir(path):
            tmp_path = path + '/' + l
            if os.path.isdir(tmp_path):
                cls.check_dir_deleted(tmp_path)
            cls._check_delete(tmp_path)

        cls._check_delete(path)

    @classmethod
    def _check_delete(cls, path):
        if not config.delete_local_file:
            return
        if path == config.path_to_watch:
            return
        path = path.replace(config.path_to_watch, '')
        client = config.client
        try:
            m = client.metadata(path)
            if m.get('is_deleted'):
                cls.delete(path)
        except:
            pass

client = Client
