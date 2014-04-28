## Drop2PI ##

[![Build Status](https://travis-ci.org/GuoJing/Drop2PI.png?branch=master)](https://travis-ci.org/GuoJing/Drop2PI) [![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/GuoJing/drop2pi/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Sorry for bad English.

This is a very simple tool to sync files between Dropbox and Raspberry PI. In fact this command tools can used any system running on Python.

But I only wants to sync files to Raspberry PI. So I called this Dropbox to PI.


## Overall ##

1. download the file and folder auto.
2. modify the folder, auto sync to Dropbox.
3. delete the file or folder which deleted in Dropbox server auto.


## Install ##

You can install by download the source or

	python setup.py install
	
or

	pip install d2pi

## V 0.0.9 ##

**Changes**:

1. add a very simple cache, it's dict in memory.
2. better sync_download

`sync_download` will be:

1. check metadata and set hash to cache
2. request dropbox with hash, it no change then return cache object

this will be faster.

and remove `check_dir_deleted`, it will search all folder and sync delete status, may blocked or broken by other events. now new `sync_download` method will handle that.

If file in dropbox and status `is_deleted` is true, and files/folder exists in local, and config require remove local file, then remove local.

If file exists in server with no change, return cache object.

## V 0.0.5 ##

1. make it OO
2. replace print to logging

## V 0.0.4 ##

1. set config at ~/.d2pi/config.yml
2. new dropbox auth method (flow)


## Need to do ##

1. config the max donload file size.
2. if there is syncing event, quit update event. (see known bug)


## Packages ##

You have to install [Watchdog](https://github.com/gorakhargosh/watchdog) first.

	sudo pip install watchdog

And also download Dropbox python SDK [HERE](https://www.dropbox.com/developers/core/sdk).

	pip install dropbox

And yaml.

## Setup ##


#### init ####

	python auth.py 

or

	from d2pi import auth
	auth.auth()


You have to go to [Dropbox Develop Page](https://www.dropbox.com/developers/apps) to create a App.

After created a App, you can find the APP_KEY and APP_SECRET, ACCESS_TYPE is also needed.

you can edit your config file at `~/.d2pi/config.yml`, path_to_watch is the dir you want to watch.


#### run watching.py ####

	python watching.py
	
or

	from d2pi import watch
	watcher = watch.Watcher()
	watcher.run()

This will watch dir `PATH_TO_WATCH`, and any changes like `create`, `modify`, `delete` and `move` will change the file in Dropbox.

### My PI ###

I need to download some files in my PI, don't need to update or edit on PI. so I just need a cron running on watching.py -c.

soundbbg at gmail
