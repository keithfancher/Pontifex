#!/usr/bin/env python


import unittest

from pont import *


class TestWithSchneiersVectors(unittest.TestCase):
    """These are the test vector's from Schneier's site. Tuples in the form
    (plaintext, key, ciphertext)"""
    test_vectors = [ ("AAAAAAAAAAAAAAA", "f", "XYIUQ BMHKK JBEGY"),
                     ("AAAAAAAAAAAAAAA", "fo", "TUJYM BERLG XNDIW"),
                     ("AAAAAAAAAAAAAAA", "FOO", "ITHZU JIWGR FARMW"),
                     ("AAAAAAAAAAAAAAA", "a", "XODAL GSCUL IQNSC"),
                     ("AAAAAAAAAAAAAAA", "aa", "OHGWM XXCAI MCIQP"),
                     ("AAAAAAAAAAAAAAA", "aAa", "DCSQY HBQZN GDRUT"),
                     ("AAAAAAAAAAAAAAA", "b", "XQEEM OITLZ VDSQS"),
                     ("AAAAAAAAAAAAAAA", "bC", "QNGRK QIHCL GWSCE"),
                     ("AAAAAAAAAAAAAAA", "BCD", "FMUBY BMAXH NQXCJ"),
                     ("AAAAAAAAAAAAAAAAAAAAAAAAA", "cryptonomicon", "SUGSR SXSWQ RMXOH IPBFP XARYQ"),
                     ("SOLITAIREX", "cryptonomicon", "KIRAK SFJAN") ]

    def test_with_passphrase(self):
        for plain, key, cipher in self.test_vectors:
            deck = key_deck_with_passphrase(key)
            self.assertEqual(encrypt(plain, deck), cipher)

    def test_decrypt(self):
        for plain, key, cipher in self.test_vectors:
            deck = key_deck_with_passphrase(key)
            self.assertEqual(decrypt(cipher, deck), insert_spaces(plain))

    def test_no_passphrase(self):
        plain = "AAAAAAAAAAAAAAA"
        cipher = "EXKYI ZSGEH UNTIQ"
        deck = range(1,55)
        self.assertEqual(encrypt(plain, deck), cipher)
        self.assertEqual(decrypt(cipher, deck), insert_spaces(plain))


class TestEncryptDecrypt(unittest.TestCase):
    def test_basic_shit(self):
        """Encrypted text should decrypt properly and vice versa"""
        deck = range(1,55)
        plaintext = "hey man, how's it hangin'?"
        cleaned_plain = split_into_fives(clean_string(plaintext))
        cipher = encrypt(plaintext, deck)
        deck = range(1,55) # reset deck (damn you python mutability!)
        self.assertEqual(decrypt(cipher, deck), insert_spaces(cleaned_plain))

    def test_goin_cray_cray(self):
        deck = range(1,55)
        deck.reverse() # mix it up a bit, why not!
        plaintext = "Let's really jazz this one up! Shit! Shit, man!"
        cleaned_plain = split_into_fives(clean_string(plaintext))
        cipher = encrypt(plaintext, deck)
        deck = range(1,55)
        deck.reverse()
        self.assertEqual(decrypt(cipher, deck), insert_spaces(cleaned_plain))


class TestEncryptWithPassphrase(unittest.TestCase):
    def test_keystream_gen(self):
        """Generate proper keystream given a passphrase"""
        key = key_deck_with_passphrase("FOO")
        keystream = [8, 19, 7, 25, 20, 9, 8, 22, 32, 43, 5, 26, 17, 38, 48]
        self.assertEqual(generate_keystream(key, 15), keystream)

    def test_full_encrypt(self):
        """Plaintext encrypted properly with passphrase"""
        key = key_deck_with_passphrase("CRYPTONOMICON")
        plaintext = "SOLITAIRE"
        ciphertext = "KIRAK SFJAN"
        self.assertEqual(encrypt(plaintext, key), ciphertext)


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
        keystream = [8, 19, 7, 25, 20, 9, 8, 22, 32, 43, 5, 26, 17, 38, 48]
        plaintext = "AAAAAAAAAAAAAAA"
        ciphertext = "ITHZUJIWGRFARMW"
        self.assertEqual(encrypt_with_keystream(plaintext, keystream), ciphertext)
        keystream = [11, 4, 23, 21, 16, 15, 14, 15, 23, 20]
        plaintext = "DONOTUSEPC"
        ciphertext = "OSKJJJGTMW"
        self.assertEqual(encrypt_with_keystream(plaintext, keystream), ciphertext)


class TestDecryptWithKeystream(unittest.TestCase):
    def test_basic_shit(self):
        keystream = [4, 49, 10, 24, 8, 51, 44, 6, 4, 33]
        ciphertext = "EXKYIZSGEH"
        plaintext = "AAAAAAAAAA"
        self.assertEqual(decrypt_with_keystream(ciphertext, keystream), plaintext)
        keystream = [11, 4, 23, 21, 16, 15, 14, 15, 23, 20]
        ciphertext = "OSKJJJGTMW"
        plaintext = "DONOTUSEPC"
        self.assertEqual(decrypt_with_keystream(ciphertext, keystream), plaintext)


class TestEncrypt(unittest.TestCase):
    def test_basic_shit(self):
        plaintext = "AAAAAAAAAA"
        ciphertext = "EXKYI ZSGEH"
        deck = range(1, 55)
        self.assertEqual(encrypt(plaintext, deck), ciphertext)


class TestDecrypt(unittest.TestCase):
    def test_basic_shit(self):
        ciphertext = "EXKYI ZSGEH"
        plaintext = "AAAAA AAAAA"
        deck = range(1, 55)
        self.assertEqual(decrypt(ciphertext, deck), plaintext)


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
