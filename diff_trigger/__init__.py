from functools import wraps
from inspect import signature
from collections.abc import Mapping, Iterable
from threading import Lock
import pickle
import logging
import types

import plyvel


DBLOCK = Lock()


def expand(o):
    if isinstance(o, (str, int, float, bytes)):
        return o
    elif isinstance(o, Mapping):
        return expand(sorted(o.items()))
    elif isinstance(o, Iterable):
        l = []
        for i in o:
            l.append(expand(i))
        return tuple(l)
    else:
        return o


def make_key(func, *args, **kwargs):
    hashkey = [func.__name__]
    boundarg = signature(func).bind(*args, **kwargs)
    boundarg.apply_defaults()
    hashkey.extend(boundarg.arguments.values())
    return pickle.dumps(expand(hashkey))



class WatchDiff:
    def __init__(self, func, dbpath, callback):
        wraps(func)(self)
        self.dbpath = dbpath
        self.callback = callback

    def __call__(self, *args, **kwargs):
        key = make_key(self.__wrapped__, *args, **kwargs)
        new_data = self.__wrapped__(*args, **kwargs)
        old_data = None
        try:
            DBLOCK.acquire()
            db = plyvel.DB(self.dbpath, create_if_missing=True)
        except:
            logging.error('handle local database error')
            DBLOCK.release()
        else:
            try:
                load_data = db.get(key)
                old_data = pickle.loads(load_data) if load_data else None
                if old_data != new_data:
                    saved_data = pickle.dumps(new_data)
                    db.put(key, saved_data)
            except:
                logging.error('loading data error')
            finally:
                db.close()
                DBLOCK.release()
            try:
                if old_data and old_data != new_data:
                    logging.debug('data change from {} to {}, run callback function'.format(old_data, new_data))
                    self.callback(old_data, new_data)
            except:
                logging.error('callback function error for data change from {} to {}'.format(old_data, new_data))
        return new_data


    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def watchdiff(dbpath, callback):
    def wrapper(func):
        return WatchDiff(func, dbpath, callback)
    return wrapper

