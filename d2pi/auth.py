# -*- coding: utf-8 -*-

# pylint: disable=E0602
try:
    input = raw_input
except:
    pass
# pylint: enable=E0602

from .config import config


def warn(overwrite=False):
    print('CONFIG FILE %s ERROR, NOT APP NAME OR SECRET' % config.filename)
    print('CONFIG FILE Created at %s' % config.filename)
    print('Please make sure follow config is filled:')
    print('- app_key:       your dropbox app key')
    print('- app_secret:    your dropbox app_secret')
    print('- path_to_watch: your path to watch')
    if overwrite:
        app_key = input('Enter the app_key here: ').strip()
        app_secret = input('Enter the app_secret here: ').strip()
        path_to_watch = input('Enter the watch full path here '
                              '(like /home/guojing/somepath):')
        if not app_key:
            print('app key should not be empty')
            return
        if not app_secret:
            print('app secret should not be empty')
            return
        if not path_to_watch:
            print('path to watch should not be empty')
            return
        print('Write app_key %s, app_secret %s, path_to_watch %s '
              'to config.' % (app_key, app_secret, path_to_watch))
        config.create(app_key=app_key,
                      app_secret=app_secret,
                      path_to_watch=path_to_watch,
                      overwrite=overwrite)
    return


def auth():
    if not config.is_useable():
        warn()
        return
    from dropbox import client
    flow = client.DropboxOAuth2FlowNoRedirect(config.app_key,
                                              config.app_secret)
    authorize_url = flow.start()

    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')

    code = input('Enter the authorization code here: ').strip()

    access_token, user_id = flow.finish(code)

    config.token = (access_token, user_id)

if __name__ == '__main__':
    auth()
