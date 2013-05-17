# -*- coding: utf-8 -*-
from dropbox import client, session
from config import APP_KEY, APP_SECRET, ACCESS_TYPE, TOKEN_FILE

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

def get_session():
    return sess

def get_auth_url_and_token():
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    return url, request_token

def set_token(request_token):
    access_token = sess.obtain_access_token(request_token)
    try:
        token_file = open(TOKEN_FILE, 'w')
        token_file.write('%s|%s' % (access_token.key, access_token.secret))
        token_file.close()
    except Exception, e:
        token_file.close()
        print 'Can not write to file %s - Error %s' % (TOKEN_FILE, e)

def get_token():
    try:
        token_file = open(TOKEN_FILE)
        token_key, token_secret = token_file.read().split('|')
        token_file.close()
        return token_key, token_secret
    except Exception, e:
        token_file.close()
        print 'Can not read token file %s - Error %s' % (TOKEN_FILE, e)
        return None, None

def get_client():
    token_key, token_secret = get_token()
    if token_key and token_secret:
        sess.set_token(token_key, token_secret)
        c = client.DropboxClient(sess)
        return c

def parse_file_dir(file_path):
    '''
    input:  /some1/some2/filename.txt
    return: filename.txt
    '''
    f = file_path.split('/')
    return f[-1]

