# -*- coding: utf-8 -*-

'''
    simpleirc.parser
    ----------------

    Regex line parser.
'''

import re

re_line = re.compile('^(\:\S+.*?|)([^\: ]\S+.*?|)([^\: ]\S+.*?|)(\:\S+.*?|)$')


def parse_line(state, l):
    parsed = re_line.findall(l)
    if not parsed:
        return state

    parsed = parsed[0]

    # cleanup things that the regex wasn't able to
    parsed = map(lambda e: e[1:] if e.startswith(':') else e, parsed)
    parsed = map(lambda e: e.strip(), parsed)

    state['prefix'] = parsed[0]
    state['command'] = parsed[1]
    state['params'] = parsed[2]
    state['crlf'] = parsed[3]

    state['line'] = l
    return state
