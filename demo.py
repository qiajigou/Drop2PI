# -*- coding: utf-8 -*-

import os
import sys

welcome = """
**************************
Thanks for using d2pi
    this is a demo

Thanks to my girlfriend
without you I would make
it faster.

But I still love you. :)
**************************
"""

downloader = """
And this is downloader
Downloader will only download files
Anything you do in local will do nothing to server.
"""

uploader = """
And this is uploader
Uploader will only upload files.
"""

auto_downloader = """
This is default watcher

This watcher will watch all events in local like:

- NEW FILE/DIR
- DELETE FILE/DIR
- MOVE FILE/DIR

And it will auto download files to local.

I will cache downloaded files and will be flushed
when file statue changed.

It have a simple lock, if upload is working,
download will be blocked.

The same, if auto download is working, then
new file could create but upload event will be block.

Because this is a simple tool, will not connect to
any server and not be pushed by any server

So we don't have better way to solve that problem.

Why dont't we add a queue and insert event to a queue?

This tool is using watchdog, everytime download a file
it will cause a create file event. Then we will upload
file again, with same content.
"""

simple_watcher = """
This is the watcher with no auto download.

It will download and sync to server at first time
Then it will not download automatically.

This watcher will watch all events in local like:

- NEW FILE/DIR
- DELETE FILE/DIR
- MOVE FILE/DIR
"""

help = """
Try:

downloader: demo.py -d
uploader:   demo.py -u
watcher:    demo.py -w
"""


def demo():
    print(welcome)
    args = sys.argv
    args = args[1:]
    print(help)
    from d2pi.config import config
    if not config.is_useable():
        from d2pi.auth import warn
        warn(overwrite=True)
        print('Done! Run again to auth!')
    elif not config.has_token():
        from d2pi.auth import auth
        auth()
        print('Success! Run demo again!')
    else:
        if args and args[0] == '-d':
            print(downloader)
            from d2pi.watch import downloader
            downloader.run()
        elif args and args[0] == '-u':
            print(uploader)
            from d2pi.watch import uploader
            uploader.run()
        elif args and args[0] == '-w':
            print(auto_downloader)
            from d2pi.watch import watcher
            watcher.run()
        else:
            print(simple_watcher)
            from d2pi.watch import watcher
            watcher.auto_download = False
            watcher.run()

if __name__ == '__main__':
    try:
        pid = str(os.getpid())
        pidfile = '/tmp/d2pi.pid'
        if os.path.isfile(pidfile):
            print('d2pi already exists, exiting %s' % pidfile)
            sys.exit()
        else:
            file(pidfile, 'w').write(pid)
        demo()
    except Exception as e:
        print(e)
    finally:
        try:
            os.unlink(pidfile)
        except:
            pass
