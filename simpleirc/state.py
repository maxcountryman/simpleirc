# -*- coding: utf-8 -*-

'''
    simpleirc.state
    ---------------

    Evil, mutable state.
'''

_irc_state = {'channels': [],
              'prefix': None,
              'command': None,
              'params': None,
              'crlf': None,
              'line': None}


def _get_irc_state():
    return _irc_state
