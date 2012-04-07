#!/usr/bin/env python


import unittest

from pont import insert_spaces
from pont import clean_string
from pont import split_into_fives
from pont import move_card_down
from pont import keystream_step_1
from pont import keystream_step_2
from pont import keystream_step_3
from pont import keystream_step_4
from pont import get_keystream_num
from pont import generate_keystream
from pont import encrypt_with_keystream
from pont import encrypt
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


class TestGetKeystreamNum(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = [1, 2, 5, 4, 6, 3]
        result = 2
        self.assertEqual(get_keystream_num(in_deck), result)


class TestGenerateKeystream(unittest.TestCase):
    def test_basic_shit(self):
        in_deck = range(1, 55)
        keystream = [4, 49, 10, 24, 8, 51, 44, 6, 4, 33]
        self.assertEqual(generate_keystream(in_deck, 10), keystream)


class TestEncryptWithKeystream(unittest.TestCase):
    def test_basic_shit(self):
        keystream = [4, 49, 10, 24, 8, 51, 44, 6, 4, 33]
        plaintext = "AAAAAAAAAA"
        ciphertext = "EXKYIZSGEH"
        self.assertEqual(encrypt_with_keystream(plaintext, keystream), ciphertext)
        keystream = [11, 4, 23, 21, 16, 15, 14, 15, 23, 20]
        plaintext = "DONOTUSEPC"
        ciphertext = "OSKJJJGTMW"
        self.assertEqual(encrypt_with_keystream(plaintext, keystream), ciphertext)


class TestEncrypt(unittest.TestCase):
    def test_basic_shit(self):
        plaintext = "AAAAAAAAAA"
        ciphertext = "EXKYI ZSGEH"
        deck = range(1, 55)
        self.assertEqual(encrypt(plaintext, deck), ciphertext)


class TestMoveCardDown(unittest.TestCase):
    # tuples in the form (indeck, outdeck, n)
    test_decks = [ ( [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], 1),
                   ( [1, 2, 3, 4, 5], [2, 3, 4, 5, 1], 4),
                   ( [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], 5),
                   ( [0, 2, 3, 4, 1], [0, 1, 2, 3, 4], 1) ]

    def test_basic_shit(self):
        for indeck, outdeck, n in self.test_decks:
            self.assertEqual(move_card_down(indeck, 1, n), outdeck)


class TestCleanString(unittest.TestCase):
    # in the form (instring, outstring)
    test_strings = [("hello 1 `';!!!    man,", "HELLO1MAN"),
                    ("\t\t!!!!!!    b 4,,;'][()+lls", "B4LLS")]

    def test_basic_shit(self):
        for instring, outstring in self.test_strings:
            self.assertEqual(clean_string(instring), outstring)


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
    test_strings = [("hey there", "HEYTHEREXX"),
                    ("hey", "HEYXX"),
                    ("do not use PC", "DONOTUSEPC"),
                    ("welcome home", "WELCOMEHOMEXXXX")]

    def test_basic_shit(self):
        for instring, outstring in self.test_strings:
            self.assertEqual(split_into_fives(instring), outstring)


if __name__ == "__main__":
    unittest.main()
