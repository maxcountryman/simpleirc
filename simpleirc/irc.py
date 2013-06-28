# -*- coding: utf-8 -*-

'''
    simpleirc.irc
    -------------

    IRC commands.
'''

from simpleirc.io import put_line


def privmsg(target, message):
    return put_line('PRIVMSG {target} :{message}'.format(target=target,
                                                         message=message))


def join(channel):
    return put_line('JOIN ' + channel)


def part(channel):
    return put_line('PART ' + channel)


def quit(message=None):
    put_line('QUIT ' + (message or ''))


def nick(nick):
    put_line('NICK ' + nick)


def me(target, action):
    privmsg(target, chr(1) + 'ACTION ' + action + chr(1))
