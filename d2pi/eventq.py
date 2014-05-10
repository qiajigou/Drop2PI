# -*- coding: utf-8 -*-
# this is a simple event queue

_queue = None
try:
    # python 2
    import Queue as _queue
except:
    # python 3
    import queue as _queue


class EventQueue(object):
    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self._q = _queue.Queue(maxsize=maxsize)

    def put(self, event, callback):
        self._q.put((event, callback))

    def run(self):
        while(not self._q.empty()):
            e, fun = self._q.get()
            fun(e)

if __name__ == '__main__':
    q = EventQueue(maxsize=10)

    def _callback(event):
        assert event == 1
    event = 1
    q.put(event, _callback)
    q.run()
