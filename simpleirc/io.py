# -*- coding: utf-8 -*-

'''
    simpleirc.io
    ------------

    I/O logic.
'''

import json
import logging
import os

from Queue import Queue
from socket import AF_UNIX, socket, SOCK_DGRAM
from thread import start_new_thread as new_thread

logging.basicConfig(level=logging.DEBUG)

BUFSIZE = 4096
DOMAIN_SOCKET_PATH = '/tmp/simpleirc.sock'

_i = Queue()
_o = Queue()

_domain_sockets = set()


# TODO: fix logging


def get_line():
    return _i.get(block=True)


def put_line(line):
    logging.info('>>> ' + line)
    return _o.put(line + '\r\n')


def read_lines(s, bufsize):  # pragma: no cover
    while True:
        map(lambda l: (logging.info(l), _i.put(l)),
            s.recv(bufsize).split('\r\n')[:-1])


def write_lines(s):  # pragma: no cover
    while True:
        s.send(_o.get(block=True))


def domain_listen():  # pragma: no cover
    if os.path.exists(DOMAIN_SOCKET_PATH):
        os.unlink(DOMAIN_SOCKET_PATH)

    s = socket(AF_UNIX, SOCK_DGRAM)
    s.bind(DOMAIN_SOCKET_PATH)

    while True:
        lines = s.recv(BUFSIZE).split('\r\n')[:-1]
        map(lambda l: new_thread(_handle_domain_line, (l,)), lines)


def get_domain_sockets():
    return _domain_sockets


def _handle_domain_line(l):
    import irc

    try:
        l = json.loads(l)
    except ValueError:
        logging.debug(l, exc_info=True)
        return

    sock_path = l.get('register')

    if sock_path is not None:
        get_domain_sockets().add(sock_path)
        return

    for k, v in l.iteritems():
        if hasattr(irc, k):
            if isinstance(v, list):
                getattr(irc, k)(*l[k])
