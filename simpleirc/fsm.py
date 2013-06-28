# -*- coding: utf-8 -*-

'''
    simpleirc.fsm
    -------------

    Finite state machine states and logic.
'''

import errno
import json
import logging

from functools import partial
from socket import AF_UNIX, error, socket, SOCK_DGRAM

from simpleirc.callbacks import get_callbacks
from simpleirc.io import get_domain_sockets, get_line, put_line
from simpleirc.parser import parse_line


# The zero state bootstraps the state transitions, leading with `_register`.


def zero_state(state):
    '''
    Bootstraps the state machine by kicking off the initial state, i.e.
    `_register`.

    States are defined as generators which yield generators. The yielded
    generator is considered the next state. This function is responsible for
    consuming the generator states by calling ``next`` over them, successively.
    The current state is bound to a variable `s` which is passed to ``next``
    and in tandem the return value of this call is bound to `s`, this
    process is then repeated indefinitely.
    '''
    s = _register(state.copy(), _take_line)
    while True:
        s = next(s)


# States


def _register(state, next_state):
    put_line('NICK ' + state['nick'])
    put_line('USER ' + state['nick'] + ' 0 * :' + state['realname'])
    yield next_state(state, _apply_callbacks)


# take_line -> apply_callbacks
def _take_line(_, next_state):
    from simpleirc.connection import _get_irc_state
    yield next_state(parse_line(_get_irc_state(), get_line()),
                     _domain_send)


# apply_callbacks -> domain_send
def _apply_callbacks(state, next_state):
    # ensure we copy a new dictionary object here so that we do not recurse
    # infinitely on the same dictionary and hit maximum recursion depth
    #
    # callbacks are currently applied synchronously
    map(lambda f: f(state.copy()), get_callbacks().itervalues())
    yield next_state(state, _take_line)


# domain_send -> take_line
def _domain_send(state, next_state):
    map(partial(_get_domain_socket, state), get_domain_sockets())
    yield next_state(state, _apply_callbacks)


def _get_domain_socket(state, sock_path):
    s = socket(AF_UNIX, SOCK_DGRAM)
    try:
        s.sendto(json.dumps(state) + '\r\n', sock_path)
    except error, e:
        if e.errno == errno.ENOBUFS:
            message = 'Buffer full at {sock_path}; dropping line'
            logging.warn(message.format(sock_path=sock_path))
            pass
