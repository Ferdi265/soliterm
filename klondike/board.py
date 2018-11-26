from enum import Enum
from random import shuffle
from typing import *

import json

from .data import *

def display_stack_top(stack: List[Card], default: str) -> str:
    if len(stack) == 0:
        return default
    else:
        return str(stack[-1])

class BoardCard:
    card: Card
    revealed: bool

    def __init__(self, card: Card, revealed: bool):
        self.card = card
        self.revealed = revealed

    def __str__(self):
        if self.revealed:
            return str(self.card)
        else:
            return Card.BLANK

    def __repr__(self):
        return "BoardCard({}, {})".format(repr(self.card), self.revealed)

class Board:
    deck: List[Card]
    drop: List[Card]
    foundation: Tuple[List[Card], List[Card], List[Card], List[Card]]
    board: Tuple[
        List[BoardCard], List[BoardCard], List[BoardCard], List[BoardCard],
        List[BoardCard], List[BoardCard], List[BoardCard]
    ]

    def __init__(self):
        self.deck = [Card(Suit(s), Value(v)) for v in range(1, 14) for s in range(4)]
        shuffle(self.deck)

        self.drop = []
        self.foundation = ([], [], [], [])
        self.board = ([], [], [], [], [], [], [])

        self.deal()

    @staticmethod
    def deserialize(ser: str):
        board = Board()
        dic = json.loads(ser)
        try:
            board.deck = [Card(Suit(c['suit']), Value(c['value'])) for c in dic['deck']]
            board.drop = [Card(Suit(c['suit']), Value(c['value'])) for c in dic['drop']]
            board.foundation = tuple([
                [Card(Suit(c['suit']), Value(c['value'])) for c in f]
                    for f in dic['foundation']
            ])
            board.board = tuple([
                [BoardCard(Card(Suit(c['suit']), Value(c['value'])), c['revealed']) for c in s]
                    for s in dic['board']
            ])
        except KeyError:
            raise ValueError("could not load game")

        return board

    def serialize(self):
        return json.dumps({
            'deck': [{ 'suit': c.suit.value, 'value': c.value.value } for c in self.deck],
            'drop': [{ 'suit': c.suit.value, 'value': c.value.value } for c in self.drop],
            'foundation': [
                [{ 'suit': c.suit.value, 'value': c.value.value } for c in f]
                    for f in self.foundation
            ],
            'board': [
                [{ 'suit': c.card.suit.value, 'value': c.card.value.value, 'revealed': c.revealed } for c in s]
                    for s in self.board
            ],
        })

    def draw(self) -> Optional[Card]:
        if len(self.deck) > 0:
            return self.deck.pop()
        elif len(self.drop) > 0:
            self.deck = list(reversed(self.drop))
            self.drop = []
            return self.draw()
        else:
            return None

    def deal(self):
        for i in range(len(self.board)):
            for j in range(i + 1):
                self.board[i].append(BoardCard(self.draw(), False))
            self.board[i][-1].revealed = True

    def draw_deck(self):
        card = self.draw()
        if card != None:
            self.drop.append(card)

    def move_to_board_allowed(self, moved_cards: List[Card], target: List[BoardCard]) -> bool:
        #print(">> move to board allowed")
        #print("  moved cards:")
        #for c in moved_cards:
        #    print("    {}".format(repr(c)))
        #print("  target:")
        #for c in target:
        #    print("    {}".format(repr(c)))

        if len(target) == 0:
            return moved_cards[0].value == Value.KING

        target_top = target[-1]
        bottom_card = moved_cards[0]
        return (
            target_top.revealed and
            bottom_card.suit.color() != target[-1].card.suit.color() and
            bottom_card.value.value == target[-1].card.value.value - 1
        )

    def move_to_board(self, moved_cards: List[Card], target: List[BoardCard]):
        if not self.move_to_board_allowed(moved_cards, target):
            raise ValueError("that move is not allowed")

        bcards = [BoardCard(c, True) for c in moved_cards]
        target += bcards

    def move_to_foundation_allowed(self, card: Card) -> bool:
        foundation = self.foundation[card.suit.value]
        if len(foundation) == 0:
            req_val = 1
        else:
            req_val = foundation[-1].value.value + 1

        return card.value.value == req_val

    def move_to_foundation(self, card: Card):
        if not self.move_to_foundation_allowed(card):
            raise ValueError("that move is not allowed")

        self.foundation[card.suit.value].append(card)

    def board_substack_allowed(self, index: int, stack: List[BoardCard]):
        #print(">> board substack allowed")
        #print("  index: {}".format(index))
        #print("  stack:")
        #for c in stack:
        #    print("    {}".format(repr(c)))

        if len(stack) == 0 or index == 0:
            return False

        last = stack[-1]
        if not last.revealed:
            return False

        for bcard in reversed(stack[-index:-1]):
            if (
                not bcard.revealed or
                last.card.suit.color() == bcard.card.suit.color() or
                last.card.value.value != bcard.card.value.value - 1
            ):
                return False
            last = bcard

        return True

    def board_substack_remove(self, index: int, src: List[BoardCard]):
        if not self.board_substack_allowed(index, src):
            raise ValueError("cannot remove that substack")

        del src[-index:]
        if len(src) > 0:
            src[-1].revealed = True

    def move_foundation_to_board(self, suit: Suit, dest: List[BoardCard]):
        if len(self.foundation[suit.value]) == 0:
            raise ValueError("no cards in that foundation zone")

        self.move_to_board(self.foundation[suit.value][-1:], dest)
        del self.foundation[suit.value][-1:]

    def move_drop_to_board(self, dest: List[BoardCard]):
        if len(self.drop) == 0:
            raise ValueError("no cards in drop zone")

        self.move_to_board(self.drop[-1:], dest)
        del self.drop[-1:]

    def move_drop_to_foundation(self):
        if len(self.drop) == 0:
            raise ValueError("no cards in drop zone")

        self.move_to_foundation(self.drop[-1])
        del self.drop[-1:]

    def move_board_to_board_allowed(self, index: int, src: List[BoardCard], dest: List[BoardCard]):
        #print(">> move board to board allowed")
        #print("  index: {}".format(index))
        #print("  src:")
        #for c in src:
        #    print("    {}".format(repr(c)))
        #print("  dest:")
        #for c in dest:
        #    print("    {}".format(repr(c)))

        if not self.board_substack_allowed(index, src):
            return False

        cards = [bc.card for bc in src[-index:]]
        return self.move_to_board_allowed(cards, dest)

    def move_board_to_board(self, index: int, src: List[BoardCard], dest: List[BoardCard]):
        if not self.board_substack_allowed(index, src):
            raise ValueError("cannot move that substack")

        cards = [bc.card for bc in src[-index:]]
        self.move_to_board(cards, dest)
        self.board_substack_remove(index, src)

    def move_board_to_foundation_allowed(self, src: List[BoardCard]):
        if not self.board_substack_allowed(1, src):
            return False

        return self.move_to_foundation_allowed(src[-1].card)

    def move_board_to_foundation(self, src: List[BoardCard]):
        if not self.board_substack_allowed(1, src):
            raise ValueError("cannot move that substack")

        self.move_to_foundation(src[-1].card)
        self.board_substack_remove(1, src)

    def game_won(self) -> bool:
        return min(map(len, self.foundation)) == 13

    def display(self):
        bg = colorama.Back.LIGHTWHITE_EX
        fg = colorama.Fore.BLACK
        rbg = colorama.Back.RESET
        rfg = colorama.Fore.RESET

        header = (
            "{bg}┌────────────────────┐{rbg}\n"
            "{bg}│{deck} {drop}    {f[0]} {f[1]} {f[2]} {f[3]}│{rbg}\n"
            "{bg}│                    │{rbg}\n"
            "{bg}│{fg}01 02 03 04 05 06 07{rfg}│{rbg}\n"
        ).format(
            deck = Card.BLANK if len(self.deck) > 0 else Card.SLOT,
            drop = display_stack_top(self.drop, Card.SLOT),
            f = [display_stack_top(s, Card.SLOT) for s in self.foundation],
            bg = bg, fg = fg, rbg = rbg, rfg = rfg
        )

        template_row = (
            "{bg}│{b[0]} {b[1]} {b[2]} {b[3]} {b[4]} {b[5]} {b[6]}│{rbg}\n"
        )

        body = ""
        for i in range(max(map(len, self.board))):
            default = Card.SLOT if i == 0 else Card.NONE
            body += template_row.format(
                b = [str(s[i]) if len(s) > i else default for s in self.board],
                bg = bg, rbg = rbg
            )

        body += "{bg}└────────────────────┘{rbg}\n".format(
            bg = bg, rbg = rbg
        )

        return header + body
