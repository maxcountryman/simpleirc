#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    simpleirc.connection
    --------------------

    IRC connection logic.
'''

import logging

from socket import socket
from ssl import wrap_socket
from thread import start_new_thread as new_thread

from simpleirc.callbacks import (_join, _nick, _part, _pong, register_callback)
from simpleirc.fsm import zero_state
from simpleirc.io import BUFSIZE, domain_listen, read_lines, write_lines
from simpleirc.state import _get_irc_state

logging.basicConfig(level=logging.DEBUG)


def register_callbacks():
    # register ping-pong functionality
    register_callback(_pong)

    # channel state callbacks
    register_callback(_join)
    register_callback(_part)
    register_callback(_nick)


def set_config(nick, user, realname):
    _irc_state = _get_irc_state()

    # registration configuration
    _irc_state['nick'] = nick
    _irc_state['user'] = user
    _irc_state['realname'] = realname

    return _irc_state


def connect(server, nick, user, realname, ssl=False, bufsize=BUFSIZE):
    s = socket()

    if ssl:
        s = wrap_socket(s)

    s.connect(server)

    _irc_state = set_config(nick, user, realname)

    register_callbacks()

    # bootstrap I/O threads
    new_thread(read_lines, (s, bufsize))
    new_thread(write_lines, (s,))

    # bootstrap FSM
    new_thread(zero_state, (_irc_state.copy(),))

    # domain socket listener
    new_thread(domain_listen, ())

    return _irc_state


def run():
    import sys

    if not sys.argv or len(sys.argv) not in (6, 7):
        print 'usage: irc.py "irc.example.com" 6667 "nick" "user" "realname" 0'
        sys.exit()

    connect(server=(sys.argv[1], int(sys.argv[2])),
            nick=sys.argv[3],
            user=sys.argv[4],
            realname=sys.argv[5],
            ssl=bool(int(sys.argv[6])) if len(sys.argv) == 7 else False)

    while True:
        pass


if __name__ == '__main__':
    run()
