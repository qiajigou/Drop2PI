## Drop2PI ##

[![Build Status](https://travis-ci.org/GuoJing/Drop2PI.png?branch=master)](https://travis-ci.org/GuoJing/Drop2PI) [![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/GuoJing/drop2pi/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Sorry for bad English.

This is a very simple tool to sync files between Dropbox and Raspberry PI. In fact this command tools can used any system running on Python.

But I only wants to sync *small* files to Raspberry PI. So I called this Dropbox to PI.

Big file is not well supported.

Try `python demo.py`.

## Install ##

Download the code and:

	python setup.py install

Or using pip:

	pip install d2pi

## Config ##

You have to go to [Dropbox Develop Page](https://www.dropbox.com/developers/apps) to create a App.

After created a App, you can find `APP_KEY` and `APP_SECRET`.

You could run demo.py three times to generate automatically:

1. First time it will ask you to fill app\_key and app\_secret and path\_to\_watch.
2. After success and run again, it will ask to auth to dropbox.
3. After success and run again, it will start demo and download files.

## Config your self ##

You can do it your self:

    from d2pi.auto import auth
    auth()

It will ask you to fill the app\_key and secret and watch path your self.

After fill up, restart terminal bash and:

    from d2pi.auto import auth
    auth()

Run again.

This will generate config automatically, remember root user's config is not the same path with normal user.

Or you can edit your config file at `~/.d2pi/config.yml`, `path_to_watch` is the dir you want to watch.

## Overall ##

In version 0.0.9.2, you can use downloader, uploader and default watcher.

downloader:

	from d2pi.watch import downloader
	downloader.run()

downloader will only download files to local automatically.

uploader:

	from d2pi.watch import uploader
	uploader.run()

uplodaer will only upload files.

watcher with auto download:

	from d2pi.watch import watcher
    watcher.run()

auto download watcher will modify every events and sync to server.

This watcher will watch all events in local like:

- NEW FILE/DIR
- DELETE FILE/DIR
- MOVE FILE/DIR

## Important ##

The watcher will do anything and watch any events, so:

It will cache downloaded files and will be flushed when file statue changed.

It have a simple lock, if upload is working, download will be blocked.

The same, if auto download is working, then new file could create but upload event will be block.

Because this is a simple tool, will not connect to any server and not be pushed by any server.

We don't have better way to solve that problem.

Why dont't we add a queue and insert event to a queue?

This tool is using watchdog, everytime download a file it will cause a create file event. Then we will upload file again, with same content.

So we need block something.

## Customize watcher ##

You can customize watcher yourself:

    def __init__(self, can_upload=True, can_download=True,
                 can_delete=True, auto_download=False):
        self.can_upload = can_upload
        self.can_download = can_download
        self.can_delete = can_delete
        self.auto_download = auto_download

So downloader is:

	downloader = Watcher(can_upload=False, can_delete=False, auto_download=True)

Any bug, please contact me at soundbbg@gmail.com.