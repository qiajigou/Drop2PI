# -*- coding: utf-8 -*-
# this is a simple event queue

import Queue as _queue


class Queue(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._q = _queue.Queue(maxsize=maxsize)

    def put(self, event, callback):
        self._q.put((event, callback))

    def run(self):
        while(not self._q.empty()):
            e, fun = self._q.get()
            fun(e)
