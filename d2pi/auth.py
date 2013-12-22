# -*- coding: utf-8 -*-

from utils import get_auth_url_and_token, set_token

url, token = get_auth_url_and_token()

print "LOGIN INTO THE URL OD ROPBOX:", url

raw_input()

set_token(token)
