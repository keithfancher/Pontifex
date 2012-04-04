#!/usr/bin/env python


import unittest

from pont import split_into_fives


class TestSplitIntoFives(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_shit(self):
        instring = "hey there"
        outstring = "HEYTH EREXX"
        self.assertEqual(instring, outstring)


if __name__ == "__main__":
    unittest.main()
