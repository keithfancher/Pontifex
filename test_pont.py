#!/usr/bin/env python


import unittest

from pont import insert_spaces
from pont import split_into_fives


class TestInsertSpaces(unittest.TestCase):

    # in the form (instring, outstring)
    test_strings = [("abcdefghijklm", "abcde fghij klm"),
                    ("hey there man", "hey t here  man"),
                    ("hey", "hey"),
                    ("abcdeabcdeabcde", "abcde abcde abcde")]

    def test_basic_shit(self):
        """a bunch of basic strings should get transformed correctly!"""
        for instring, outstring in self.test_strings:
            self.assertEqual(insert_spaces(instring), outstring)


class TestSplitIntoFives(unittest.TestCase):

    # in the form (instring, outstring)
    test_strings = [("hey there", "HEYTH EREXX"),
                    ("hey", "HEYXX"),
                    ("do not use PC", "DONOT USEPC"),
                    ("welcome home", "WELCO MEHOM EXXXX")]

    def test_basic_shit(self):
        """split into groups of five and capitalize, man"""
        for instring, outstring in self.test_strings:
            self.assertEqual(split_into_fives(instring), outstring)


if __name__ == "__main__":
    unittest.main()
