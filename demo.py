# -*- coding: utf-8 -*-

# auth
# only at first time in your program

from d2pi import auth

auth.auth()

# then

from d2pi import watch

watcher = watch.Watcher()
watcher.run()
