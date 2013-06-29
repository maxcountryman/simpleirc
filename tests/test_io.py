from base import SimpleIrcTestCase

from simpleirc.io import (_handle_domain_line, _i, _o, get_domain_sockets,
                          get_line, put_line)

from mock import patch

import json

import simpleirc.irc


class IoTestCase(SimpleIrcTestCase):
    def setUp(self):
        SimpleIrcTestCase.setUp(self)

        # reset the set each run
        get_domain_sockets().clear()

    @patch.object(simpleirc.irc, 'put_line')
    def test_handle_domain_line(self, mock_put_line):
        sock = '/tmp/foo'
        l = json.dumps({'register': sock})
        _handle_domain_line(l)
        self.assertIn(sock, get_domain_sockets())

        nick = 'bar'
        l = json.dumps({'nick': [nick]})
        _handle_domain_line(l)
        mock_put_line.assert_called_with('NICK ' + nick)

    @patch.object(simpleirc.irc, 'put_line')
    def test_handle_domain_line_bogus_input(self, mock_put_line):
        _handle_domain_line('foo')
        self.assertEqual(get_domain_sockets(), set([]))
        self.assertFalse(mock_put_line.called)

    def test_get_domain_sockets(self):
        get_domain_sockets().add('/tmp/foo')
        self.assertEqual(get_domain_sockets(), set(['/tmp/foo']))

    def test_get_line(self):
        l = 'foo'
        put_line(l)
        self.assertEqual(_o.get(), l + '\r\n')

    def test_put_line(self):
        l = 'foo\r\n'
        _i.put(l)
        self.assertEqual(get_line(), l)
