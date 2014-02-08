# -*- coding: utf-8 -*-

# DEFAULT CONFIG

AUTO_SYNC_TIME = 60 * 1
MAX_DOWNLOAD_FILE_SIZE = 1024 * 5

DELETE_LOCAL_FILE = False
DEBUG = False

# GET CONFIG FROM ~/.d2pi

import os
import yaml


def get_home(*path):
    try:
        from win32com.shell import shellcon, shell
    except ImportError:
        home = os.path.expanduser("~")
    else:
        home = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    return os.path.join(home, *path)


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


class Config(object):
    def __repr__(self):
        return '<Config %s>' % self.filename

    def __init__(self, conf, filename):
        self._conf = conf
        self.filename = filename

    @classmethod
    def get(cls, filename):
        ensure_dir(get_home('.d2pi'))
        with open(filename, 'r') as cfg:
            _conf = yaml.load(cfg)
            return cls(_conf, filename)

    @classmethod
    def create(cls, filename=None, app_key='', app_secret='',
               access_type='', token=''):
        ensure_dir(get_home('.d2pi'))
        filename = filename if filename else 'config.yml'
        filename = get_home('.d2pi', filename)
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write("""#Config of d2pi
app_key:  %s
app_secret: %s
access_type: %s
token: %s
delete_local_file: false
debug: false
auto_aync_time: 60
path_to_watch: ''
auto_check: true
""" % (app_key, app_secret, access_type, token))
        return cls.get(filename)

    @property
    def app_key(self):
        return str(self._conf.get('app_key', ''))

    @property
    def app_secret(self):
        return str(self._conf.get('app_secret', ''))

    @property
    def path_to_watch(self):
        path = str(self._conf.get('path_to_watch', ''))
        if path[-1] == '/':
            path = path[:-1]
        return path

    @property
    def access_type(self):
        return str(self._conf.get('access_type', 'app_folder'))

    def _get_access_token(self):
        token = self._conf.get('token', None)
        token = token or (None, None)
        if isinstance(token, tuple):
            return token
        raise Exception('Error token format')

    def _set_access_token(self, value):
        if not isinstance(value, tuple):
            raise Exception('error token')
        config = self._conf
        config['token'] = value
        new_config = yaml.dump(config)
        filename = get_home('.d2pi', self.filename)
        with open(filename, 'w') as f:
            f.write(new_config)
        self._conf = config

    token = property(_get_access_token, _set_access_token)

    @property
    def access_token(self):
        return self.token[0]

    @property
    def user_id(self):
        return self.token[1]

    @property
    def delete_local_file(self):
        return bool(self._conf.get('delete_local_file', False))

    @property
    def debug(self):
        return bool(self._conf.get('debug', False))

    @property
    def auto_check(self):
        return bool(self._conf.get('auto_check', True))

    @property
    def auto_aync_time(self):
        try:
            return int(self._conf.get('auto_aync_time', 60))
        except:
            return 60

    @property
    def client(self):
        if not self.access_token:
            return None
        from dropbox import client
        return client.DropboxClient(self.access_token)

    def is_useable(self):
        if (self.app_key and
            self.app_secret and
            self.path_to_watch and
                self.token):
            return True
        return False

config = Config.create()
