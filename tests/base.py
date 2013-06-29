import unittest

if not hasattr(unittest.TestCase, 'assertIn'):
    try:
        import unittest2 as unittest
    except:
        print('unittest2 is required to run this test suite!')
        raise


class SimpleIrcTestCase(unittest.TestCase):
    pass
