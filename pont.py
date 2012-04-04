#!/usr/bin/env python


import re


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


def main():
    print "hey"


if __name__ == "__main__":
    main()
