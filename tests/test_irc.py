from base import SimpleIrcTestCase

from simpleirc.irc import join, me, nick, part, privmsg, quit

from mock import patch

import simpleirc.irc


class IrcTestCase(SimpleIrcTestCase):
    def setUp(self):
        SimpleIrcTestCase.setUp(self)
        self.chan = '#foo'

    @patch.object(simpleirc.irc, 'put_line')
    def test_join(self, mock_put_line):
        join(self.chan)
        mock_put_line.assert_called_with('JOIN ' + self.chan)

    @patch.object(simpleirc.irc, 'put_line')
    def test_me(self, mock_put_line):
        does = 'dances'
        me(self.chan, does)
        expected = 'PRIVMSG {chan} :\x01ACTION {action}\x01'
        expected = expected.format(chan=self.chan, action=does)
        mock_put_line.assert_called_with(expected)

    @patch.object(simpleirc.irc, 'put_line')
    def test_nick(self, mock_put_line):
        n = 'bar'
        nick(n)
        mock_put_line.assert_called_with('NICK ' + n)

    @patch.object(simpleirc.irc, 'put_line')
    def test_part(self, mock_put_line):
        part(self.chan)
        mock_put_line.assert_called_with('PART ' + self.chan)

    @patch.object(simpleirc.irc, 'put_line')
    def test_privmsg(self, mock_put_line):
        message = 'foo bar baz'
        privmsg(self.chan, message)
        expected = 'PRIVMSG {target} :{message}'.format(target=self.chan,
                                                        message=message)
        mock_put_line.assert_called_with(expected)

    @patch.object(simpleirc.irc, 'put_line')
    def test_quit(self, mock_put_line):
        message = 'bye!'
        quit(message)
        mock_put_line.assert_called_with('QUIT ' + message)
