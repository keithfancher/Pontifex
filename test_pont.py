#!/usr/bin/env python


import unittest

from pont import insert_spaces
from pont import split_into_fives
from pont import move_card_down
from pont import keystream_step_1
from pont import keystream_step_2
from pont import keystream_step_3
from pont import keystream_step_4
from pont import A, B


class TestKeyStreamStep1(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = [A, 1, 2, 3]
        out_deck = [1, A, 2, 3]
        self.assertEqual(keystream_step_1(in_deck), out_deck)

    def test_looping_deck(self):
        in_deck = [1, 2, 3, A]
        out_deck = [1, A, 2, 3]
        self.assertEqual(keystream_step_1(in_deck), out_deck)


class TestKeyStreamStep2(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = [B, 1, 2, 3]
        out_deck = [1, 2, B, 3]
        self.assertEqual(keystream_step_2(in_deck), out_deck)

    def test_looping_deck(self):
        in_deck = [1, 2, 3, B]
        out_deck = [1, 2, B, 3]
        self.assertEqual(keystream_step_2(in_deck), out_deck)


class TestKeyStreamStep3(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = [1, 2, A, 3, 4, B, 5, 6]
        out_deck = [5, 6, A, 3, 4, B, 1, 2]
        self.assertEqual(keystream_step_3(in_deck), out_deck)

    def test_swapped_jokers(self):
        in_deck = [1, 2, B, 3, 4, A, 5, 6]
        out_deck = [5, 6, B, 3, 4, A, 1, 2]
        self.assertEqual(keystream_step_3(in_deck), out_deck)

    def test_empty_side(self):
        in_deck = [A, 2, 3, 4, B, 5, 6]
        out_deck = [5, 6, A, 2, 3, 4, B]
        self.assertEqual(keystream_step_3(in_deck), out_deck)

    def test_jokers_at_ends(self):
        in_deck = [A, 2, 3, 4, B]
        out_deck = [A, 2, 3, 4, B]
        self.assertEqual(keystream_step_3(in_deck), out_deck)


class TestKeyStreamStep4(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = [1, 2, 5, 4, 6, 3]
        out_deck = [4, 6, 1, 2, 5, 3]
        self.assertEqual(keystream_step_4(in_deck), out_deck)
        in_deck = [3, 2, 5, 4, 6, 1]
        out_deck = [2, 5, 4, 6, 3, 1]

    def test_jokers_on_end(self):
        in_deck = [1, 2, 3, 4, A]
        out_deck = [1, 2, 3, 4, A]
        self.assertEqual(keystream_step_4(in_deck), out_deck)
        in_deck = [1, 2, 3, 4, B]
        out_deck = [1, 2, 3, 4, B]
        self.assertEqual(keystream_step_4(in_deck), out_deck)


class TestMoveCardDown(unittest.TestCase):
    # tuples in the form (indeck, outdeck, n)
    test_decks = [ ( [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], 1),
                   ( [1, 2, 3, 4, 5], [2, 3, 4, 5, 1], 4),
                   ( [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], 5),
                   ( [0, 2, 3, 4, 1], [0, 1, 2, 3, 4], 1) ]

    def test_basic_shit(self):
        for indeck, outdeck, n in self.test_decks:
            self.assertEqual(move_card_down(indeck, 1, n), outdeck)


class TestInsertSpaces(unittest.TestCase):
    # in the form (instring, outstring)
    test_strings = [("abcdefghijklm", "abcde fghij klm"),
                    ("hey there man", "hey t here  man"),
                    ("hey", "hey"),
                    ("abcdeabcdeabcde", "abcde abcde abcde")]

    def test_basic_shit(self):
        for instring, outstring in self.test_strings:
            self.assertEqual(insert_spaces(instring), outstring)


class TestSplitIntoFives(unittest.TestCase):
    # in the form (instring, outstring)
    test_strings = [("hey there", "HEYTH EREXX"),
                    ("hey", "HEYXX"),
                    ("do not use PC", "DONOT USEPC"),
                    ("welcome home", "WELCO MEHOM EXXXX")]

    def test_basic_shit(self):
        for instring, outstring in self.test_strings:
            self.assertEqual(split_into_fives(instring), outstring)


if __name__ == "__main__":
    unittest.main()
