# -*- coding: utf-8 -*-
# this is a very simple lock


def set_lock(name='_d2_lock', lock=True):
    globals()[name] = lock


def free_lock(name='_d2_lock', lock=False):
    set_lock(name=name, lock=lock)


def get_lock(name='_d2_lock'):
    if name in globals():
        return globals().get(name)
    return False


def set_upload_lock():
    set_lock(name='_d2_upload_lock')


def free_upload_lock():
    free_lock(name='_d2_upload_lock')


def get_upload_lock():
    return get_lock('_d2_upload_lock')


if __name__ == "__main__":
    assert get_lock() is False
    set_lock()
    assert get_lock() is True
    free_lock()
    assert get_lock() is False

    assert get_upload_lock() is False
    set_upload_lock()
    assert get_upload_lock() is True
    free_upload_lock()
    assert get_upload_lock() is False
