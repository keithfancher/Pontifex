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
    """Removes all but alphanumeric characters"""
    filtered = filter(lambda x: x.isalnum(), list(instring))
    return "".join(filtered)


def split_into_fives(instring):
    """Split given string into groups of five characters, separated by spaces
    and capitalized"""
    outstring = clean_string(instring)

    # add Xs so len is multiple of 5
    if len(outstring) % 5 != 0:
        num_x = 5 - (len(outstring) % 5)
        outstring = outstring + ("X" * num_x)

    # add spaces
    outstring = insert_spaces(outstring)

    return outstring.upper() # upper case


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
    if num > 26:
        return num - 26
    else:
        return num


def encrypt_with_keystream(plaintext, keystream):
    """Encrypts the plaintext given a keystream (as a list). Contrast with the
    encrypt(plaintext, deck) function, which does the real work given a keyed
    deck."""
    if len(plaintext) != len(keystream):
        return None # not sure how to handle this gracefully
    text = map(lambda x: ord(x) - 64, list(plaintext)) # convert to list of nums
    text = [fake_mod(text[i] + keystream[i]) for i in range(len(text))]
    text = map(lambda x: chr(x + 64), text) # back to chars
    return "".join(text)


def main():
    print "hey don't run this what jeez guys"


if __name__ == "__main__":
    main()
