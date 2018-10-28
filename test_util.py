from unittest import TestCase, main
from util import to_str
from tempfile import TemporaryDirectory

class MyTest(TestCase):

    def setUp(self):
        self.test_dir = TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_a(self):
        print('a', self.test_dir)

    def test_b(self):
        print('b', self.test_dir) # a different tmpdir


class UtilTestCase(TestCase):

    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self):
        # verifying a bad case
        self.assertRaises(TypeError, to_str, object)
        #to_str(object())

if __name__ == '__main__':
    main()
