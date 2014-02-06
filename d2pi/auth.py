# -*- coding: utf-8 -*-


def auth():
    from config import config
    if not config.is_useable():
        print "CONFIG FILE %s ERROR, NOT APP NAME OR SECRET" % config.filename
        return

    from dropbox import client
    flow = client.DropboxOAuth2FlowNoRedirect(config.app_key,
                                              config.app_secret)
    authorize_url = flow.start()

    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'

    code = raw_input("Enter the authorization code here: ").strip()

    access_token, user_id = flow.finish(code)

    config.token = (access_token, user_id)

if __name__ == '__main__':
    auth()
