#!/usr/bin/env python


# A and B jokers
A = 53
B = 54


def shift_deck_right(deck):
    """Circular shift of the deck, moving card on bottom back around to top"""
    return [deck[-1]] + deck[0:-1]


def insert_spaces(instring, every=5):
    """Insert spaces every "every" characters, 5 by default"""
    outstring = ""
    for i in xrange(0, len(instring), every):
        outstring = outstring + instring[i:i+every] + " "
    return outstring.strip() # gotta strip the last extraneous space


def clean_string(instring):
    """Removes all but alphanumeric characters and makes uppercase. Now it's
    ready for encryption!"""
    filtered = filter(lambda x: x.isalnum(), list(instring))
    return "".join(filtered).upper()


def split_into_fives(instring):
    """Split given string into groups of five characters. Not separated by
    spaces at this point, since we don't want spaces to be encrypted."""
    outstring = clean_string(instring)
    # add Xs so len is multiple of 5
    if len(outstring) % 5 != 0:
        num_x = 5 - (len(outstring) % 5)
        outstring = outstring + ("X" * num_x)
    return outstring


def char_to_num(char):
    """Turns a single character into an integer, 1 through 26"""
    return ord(char.upper()) - 64


def num_to_char(num):
    """Turns an integer, 1 through 26, into an uppercase character"""
    return chr(num + 64)


def chars_to_nums(string):
    """Turns a string into a list of integers, 1 through 26"""
    return map(lambda x: char_to_num(x), list(string))


def nums_to_chars(numbers):
    """Turns a list of integers 1through 26 into a string"""
    text = map(lambda x: num_to_char(x), numbers)
    return "".join(text)


def move_card_down(deck, card, n=1):
    """Moves the specifed card down n cards in the deck, looping around properly
    as specified by the algorithm"""
    out_deck = deck
    for i in xrange(n):
        index = out_deck.index(card)
        if index == len(deck) - 1: # it's on the bottom, so effectively on top
            out_deck = shift_deck_right(out_deck)
            index = 0 # once it's rotated...
        out_deck[index], out_deck[index+1] = out_deck[index+1], out_deck[index]
    return out_deck


def keystream_step_1(deck):
    """Performs step 1 of the keystream operation. Finds the A joker and moves
    it one card down. Returns modified deck."""
    return move_card_down(deck, A)


def keystream_step_2(deck):
    """Performs step 2 of the keystream operation. Finds the B joker and moves
    it two cards down. Returns modified deck."""
    return move_card_down(deck, B, 2)


def keystream_step_3(deck):
    """Step 3. Triple cut. Swap the cards above the first joker with the cards
    below the second joker."""
    # whether it's A or B is irrelevant here, you just need "top" and "bottom"
    if deck.index(A) < deck.index(B):
        top = deck.index(A)
        bot = deck.index(B)
    else:
        top = deck.index(B)
        bot = deck.index(A)
    return deck[bot+1:] + deck[top:bot+1] + deck[0:top]


def keystream_step_4(deck):
    """Step 4. Count cut. Count down the number of the bottom card, then cut
    after that card, leaving bottom card in place."""
    # either joker on the bottom leaves deck unchanged
    if deck[-1] == A or deck[-1] == B:
        return deck
    count = deck[-1] # count down number of bottom card
    return deck[count:-1] + deck[0:count] + [deck[-1]]


def get_keystream_num(deck):
    """Gets a single keystream num given a deck that has undergone steps 1
    through 4. It's steps 5 and 6, essentially. Treat top card as a number,
    count down that number into the deck. The one AFTER is the output card.
    Convert to a number, that's your keystream num. If it's a joker, start
    again from step one :( Note that this step does NOT alter the deck, so the
    deck is not returned."""
    count = deck[0]
    if count == A or count == B:
        count = 53 # either joker is 53 here
    return deck[count]


def generate_keystream(deck, length):
    """Generates a keystream given a starting deck and length of stream"""
    keystream = [] # a list?
    new_deck = deck
    for i in xrange(length):
        while True: # could really use a do/while loop, Python!
            new_deck = keystream_step_1(new_deck)
            new_deck = keystream_step_2(new_deck)
            new_deck = keystream_step_3(new_deck)
            new_deck = keystream_step_4(new_deck)
            key_num = get_keystream_num(new_deck)
            if not (key_num == A or key_num == B): # it's not a joker, break
                break
        keystream.append(key_num)
    return keystream


def fake_mod(num):
    """The solitaire algorithm uses a not-quite-mod mod function..."""
    if num > 0 and num <= 26:
        return num
    elif num % 26 == 0:
        return 26
    else:
        return num % 26


def key_deck_with_passphrase(phrase):
    """Returns a deck keyed with the given passphrase"""
    deck = range(1,55)
    clean = clean_string(phrase) # remove shit, make uppercase
    for c in clean:
        deck = keystream_step_1(deck)
        deck = keystream_step_2(deck)
        deck = keystream_step_3(deck)
        deck = keystream_step_4(deck)
        # the extra step, count cut with passphrase letter
        count = char_to_num(c)
        deck = deck[count:-1] + deck[0:count] + [deck[-1]]
    return deck


def encrypt_with_keystream(plaintext, keystream):
    """Encrypts the plaintext given a keystream (as a list). Contrast with the
    encrypt(plaintext, deck) function, which does the real work given a keyed
    deck."""
    if len(plaintext) != len(keystream):
        return None # not sure how to handle this gracefully
    text = chars_to_nums(plaintext) # convert to list of nums
    text = [fake_mod(text[i] + keystream[i]) for i in range(len(text))]
    return nums_to_chars(text) # back to chars


def decrypt_with_keystream(ciphertext, keystream):
    """Decrypts ciphertext given a keystream (as a list)"""
    if len(ciphertext) != len(keystream):
        return None
    text = chars_to_nums(ciphertext) # convert to list of nums
    text = [fake_mod(text[i] - keystream[i]) for i in range(len(text))]
    return nums_to_chars(text) # back to chars


def encrypt(plaintext, deck):
    """Encrypts the plaintext given a keyed deck. The deck is a list of
    integers from 1 to 54 representing the cards. 1 through 13 is clubs, 14
    through 26 is diamonds, 27 through 39 is hearts, and 40 through 52 is
    spades. The 'A' joker is 53 and the 'B' joker is 54."""
    cleaned = split_into_fives(plaintext) # uppercase, mult of 5, no punct
    keystream = generate_keystream(deck, len(cleaned))
    ciphertext = encrypt_with_keystream(cleaned, keystream)
    return insert_spaces(ciphertext) # space between groups of 5 chars


def decrypt(ciphertext, deck):
    """Decrypts ciphertext given a keyed deck"""
    cleaned = clean_string(ciphertext) # kill spaces
    keystream = generate_keystream(deck, len(cleaned))
    plaintext = decrypt_with_keystream(cleaned, keystream)
    return insert_spaces(plaintext) # add spaces back


def main():
    print "hey don't run this what jeez guys"


if __name__ == "__main__":
    main()
