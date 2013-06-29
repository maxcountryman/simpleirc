from base import SimpleIrcTestCase

from simpleirc.parser import parse_line


class ParserTestCase(SimpleIrcTestCase):
    def setUp(self):
        SimpleIrcTestCase.setUp(self)

        self.keys = ('prefix', 'command', 'params', 'crlf', 'line')

    def assert_keys_ok(self, s):
        map(lambda k: self.assertIn(k, s.keys()), self.keys)

    def test_parse_line(self):
        s = {}
        l = ':strangeloop.io NOTICE AUTH :*** Looking up your hostname...'
        parse_line(s, l)

        self.assert_keys_ok(s)
        self.assertEquals(s['prefix'], 'strangeloop.io')
        self.assertEquals(s['command'], 'NOTICE')
        self.assertEquals(s['params'], 'AUTH')
        self.assertEquals(s['crlf'], '*** Looking up your hostname...')

        l = 'PING :strangeloop.io'
        parse_line(s, l)
        self.assert_keys_ok(s)
        self.assertEquals(s['prefix'], '')
        self.assertEquals(s['command'], 'PING')
        self.assertEquals(s['params'], '')
        self.assertEquals(s['crlf'], 'strangeloop.io')

    def test_parse_empty_line(self):
        s = {}
        parse_line(s, '')
        self.assert_keys_ok(s)

    def test_parse_bogus_line(self):
        # NOTE: This is an odd case that really shouldn't happen; should be
        # tracked down.
        s = {}
        parse_line(s, ' ')
        self.assertEqual(s, {})
