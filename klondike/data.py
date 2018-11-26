from enum import Enum
from typing import *

import colorama

class Color(Enum):
    RED = 0
    BLACK = 1

class Value(Enum):
    ACE = 1
    C2 = 2
    C3 = 3
    C4 = 4
    C5 = 5
    C6 = 6
    C7 = 7
    C8 = 8
    C9 = 9
    C10 = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def next(self):
        if self == Value.KING:
            return None
        else:
            return Value(self.value + 1)

    def prev(self):
        if self == Value.ACE:
            return None
        else:
            return Value(self.value - 1)

    def unicode_value(self) -> int:
        if self.value > Value.JACK.value:
            return self.value + 1
        else:
            return self.value

    def __repr__(self):
        return self.name

class Suit(Enum):
    HEARTS = 0
    CLUBS = 1
    DIAMONDS = 2
    SPADES = 3

    def color(self) -> Color:
        return Color.RED if self.value % 2 == 0 else Color.BLACK

    def unicode_symbol(self) -> int:
        return {
            Suit.HEARTS: 0x2665,
            Suit.CLUBS: 0x2663,
            Suit.DIAMONDS: 0x2666,
            Suit.SPADES: 0x2660
        }[self]

    def unicode_base(self) -> int:
        return {
            Suit.HEARTS: 0x1F0B0,
            Suit.CLUBS: 0x1F0D0,
            Suit.DIAMONDS: 0x1F0C0,
            Suit.SPADES: 0x1F0A0
        }[self]

    def __repr__(self):
        return self.name

class Card:
    NONE: str = colorama.Fore.RESET + "  "
    BLANK: str = colorama.Fore.GREEN + chr(Suit.SPADES.unicode_base()) + colorama.Fore.RESET
    SLOT: str = chr(Suit.SPADES.unicode_base())

    suit: Suit
    value: Value

    def __init__(self, suit: Suit, value: Value):
        self.suit = suit
        self.value = value

    def next(self):
        nextv = self.value.next()
        if nextv == None:
            return None

        return Card(self.suit, nextv)

    def prev(self):
        prevv = self.value.prev()
        if prevv == None:
            return None

        return Card(self.suit, prevv)

    def __str__(self) -> str:
        if self.suit.color() == Color.RED:
            c = colorama.Fore.RED
        else:
            c = colorama.Fore.BLACK

        return c + chr(self.suit.unicode_base() + self.value.unicode_value()) + colorama.Fore.RESET

    def __repr__(self):
        return "Card({}, {})".format(repr(self.suit), repr(self.value))
