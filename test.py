import unittest
from diff_trigger import watchdiff, make_key
import logging
import shutil
import os

logging.basicConfig(level=logging.DEBUG)

flag = 0
db = '/tmp/testdata'
tret = None


def trigger(old, new):
    global tret
    logging.info('data change from {} to {}'.format(old, new))
    tret = (old, new)


def test_key(a, b=2, **kwargs):
    pass


@watchdiff(dbpath=db, callback=trigger)
def t(a, b):
    global flag
    return a + b + flag


class TestClass:
    @watchdiff(dbpath=db, callback=trigger)
    def t(self, a, b):
        global flag
        ret = a + b + flag
        return ret


class TestCase(unittest.TestCase):
    def setUp(self):
        global flag
        global tret
        flag = 0
        tret = None
        if os.path.isdir(db):
            shutil.rmtree(db)

    def test_keyorder(self):
        k1 = make_key(test_key, 1, 2, c=3)
        k2 = make_key(test_key, b=2, a=1, c=3)
        k3 = make_key(test_key, c=3, b=2, a=1)
        k4 = make_key(test_key, a=1, c=3)
        self.assertEqual(k1, k2)
        self.assertEqual(k2, k3)
        self.assertEqual(k3, k4)

    def test_dictkey(self):
        k1 = make_key(test_key, {1:2, 3:4})
        k2 = make_key(test_key, {3:4, 1:2})
        self.assertEqual(k1, k2)

    def test_callback_not_run(self):
        origin = tret
        t(1, 2)
        t(1, 2)
        self.assertEqual(origin, tret)


    def test_callback_run(self):
        global flag
        origin = tret
        t(3, 4)
        flag = 1
        t(3, 4)
        self.assertNotEqual(origin, tret)


    def test_method_callback_not_run(self):
        origin = tret
        c = TestClass()
        c.t(1, 2)
        c.t(b=2, a=1)
        self.assertEqual(origin, tret)

    def test_method_callback_run(self):
        global flag
        origin = tret
        c = TestClass()
        c.t(5, 4)
        flag = 1
        c.t(5, 4)
        self.assertNotEqual(origin, tret)


if __name__ == '__main__':
    unittest.main()

