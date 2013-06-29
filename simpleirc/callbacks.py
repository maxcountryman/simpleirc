# -*- coding: utf-8 -*-

'''
    simpleirc.callbacks
    -------------------

    Callback logic.
'''

from simpleirc.io import put_line
from simpleirc.state import _get_irc_state

_callbacks = {}


def register_callback(f):
    assert hasattr(f, '__call__')
    _callbacks[f.__name__] = f


def get_callbacks():
    return _callbacks


def _pong(state):
    if state['command'] == 'PING':
        put_line(state['line'].replace('PING', 'PONG'))


# NOTA BENE: The following callbacks mangle the global IRC state: this is so we
# can keep track of which channels we are in and who populates them. In
# practice, the global state should NEVER be altered like this. What we are
# doing here is strictly for internal callers and generally speaking not a good
# idea.

_irc_state = _get_irc_state()


def _join(state):
    if state['command'] == 'JOIN' and \
            state['prefix'].startswith(state['nick']):
        chan = state['crlf']
        _irc_state['channels'].append({chan: []})

    elif state['command'] == 'JOIN':
        chan = state['crlf']
        nick = state['prefix'].split('!', 1)[0]
        for i, c in enumerate(state['channels']):
            if chan in c:
                _irc_state['channels'][i][chan].append(nick)

    elif state['command'] == '353':  # names list
        names = state['crlf'].split()
        chan = state['params'].split(' = ')[-1]
        for i, c in enumerate(state['channels']):
            if chan in c:
                _irc_state['channels'][i][chan] = names


def _part(state):
    if state['command'] == 'PART' and \
            state['prefix'].startswith(state['nick']):
        _irc_state['channels'] = filter(lambda c: state['params'] not in c,
                                        _irc_state['channels'])

    elif state['command'] == 'PART':
        chan = state['params']
        nick = state['prefix'].split('!', 1)[0]
        for i, c in enumerate(state['channels']):
            if chan in c:
                _irc_state['channels'][i][chan].remove(nick)


def _nick(state):
    if state['command'] == 'NICK':
        new = state['crlf']
        if state['prefix'].startswith(state['nick']):
            _irc_state['nick'] = new

        nick = state['prefix'].split('!', 1)[0]
        for i, c in enumerate(_irc_state['channels']):
            if nick in c.values()[0]:
                for k in _irc_state['channels'][i].iterkeys():
                    _irc_state['channels'][i][k].remove(nick)
                    _irc_state['channels'][i][k].append(new)
