#!/usr/bin/env python


import re


# This will never change, obviously
DECK_SIZE = 54

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


def split_into_fives(instring):
    """Split given string into groups of five characters, separated by spaces
    and capitalized"""
    outstring = re.sub(r'\s', '', instring) # strip all whitespace

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


def main():
    key = range(1, DECK_SIZE+1) # initial state of the deck
    deck = key

    print "hey"


if __name__ == "__main__":
    main()
