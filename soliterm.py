from __future__ import print_function

from enum import Enum
from klondike import *

import os
import sys
import readline

b = Board()

class Location(Enum):
    HEARTS = 0
    CLUBS = 1
    DIAMONDS = 2
    SPADES = 3
    DROP = 4
    FOUNDATION = 5

SUITS = [Location.HEARTS, Location.CLUBS, Location.DIAMONDS, Location.SPADES, Location.FOUNDATION]

locations = {
    "drop": Location.DROP,
    "d": Location.DROP,

    "foundation": Location.FOUNDATION,
    "f": Location.FOUNDATION,

    "hearts": Location.HEARTS,
    "heart": Location.HEARTS,
    "h": Location.HEARTS,

    "clubs": Location.CLUBS,
    "club": Location.CLUBS,
    "c": Location.CLUBS,

    "diamonds": Location.DIAMONDS,
    "diamond": Location.DIAMONDS,
    "dia": Location.DIAMONDS,

    "spades": Location.SPADES,
    "spade": Location.SPADES,
    "s": Location.SPADES
}

def parse_loc(arg):
    if arg in locations:
        return locations[arg]
    elif all(map(lambda c: c in "0123456789", arg)):
        try:
            i = int(arg, 10)
            if i < 8:
                return i - 1
        except:
            pass

def cmd_move(args):
    if len(args) == 2:
        src_arg = args[0]
        dest_arg = args[1]
    elif len(args) == 3 and args[1] == "to":
        src_arg = args[0]
        dest_arg = args[2]
    else:
        return "move: invalid usage: see help\n"

    src = parse_loc(src_arg)
    if src == None:
        return "move: invalid source: see help\n"
    dest = parse_loc(dest_arg)
    if dest == None:
        return "move: invalid destination: see help\n"

    if src == Location.FOUNDATION:
        return "move: cannot move from foundation, which suit?\n"
    elif dest == Location.DROP:
        return "move: cannot move into drop zone\n"

    try:
        if dest in SUITS:
            if src in SUITS:
                return "move: cannot move foundation into foundation\n"
            elif src == Location.DROP:
                b.move_drop_to_foundation()
            else:
                b.move_board_to_foundation(b.board[src])
        else:
            if src in SUITS:
                b.move_foundation_to_board(Suit(src.value), b.board[dest])
            elif src == Location.DROP:
                b.move_drop_to_board(b.board[dest])
            else:
                for i in range(1, len(b.board[src]) + 1):
                    if b.move_board_to_board_allowed(i, b.board[src], b.board[dest]):
                        b.move_board_to_board(i, b.board[src], b.board[dest])
                        return
                return "move: no valid move for that stack\n"
    except ValueError as e:
        return "move: {}\n".format(e)

def cmd_auto(args):
    if len(args) != 0:
        return "auto: invalid usage: see help\n"
    else:
        none_found = True
        found = True
        while found:
            found = False
            if b.move_drop_to_foundation_allowed():
                none_found = False
                found = True
                b.move_drop_to_foundation()
            for i in range(len(b.board)):
                if b.move_board_to_foundation_allowed(b.board[i]):
                    none_found = False
                    found = True
                    b.move_board_to_foundation(b.board[i])
                    redraw()
        if none_found:
            return "auto: nothing to do\n"

def cmd_draw(args):
    if len(args) != 0:
        return "draw: invalid usage: see help\n"
    else:
        b.draw_deck()

def cmd_exit(args):
    if len(args) != 0:
        return "exit: invalid usage: see help\n"
    else:
        remove_autosave()
        sys.exit(0)

def cmd_restart(args):
    global b
    if len(args) != 0:
        return "restart: invalid usage: see help\n"
    else:
        ans = None
        while ans != "" and ans != "y" and ans != "n":
            ans = input("Do you really want to restart? [y/N] ").lower()

        if ans == "y":
            b = Board()

def cmd_save(args):
    if len(args) != 1:
        return "save: invalid usage: see help\n"
    else:
        try:
            with open(args[0], "w") as f:
                f.write(b.serialize())
            return "save: saved game to file {}\n".format(args[0])
        except Exception as e:
            return "save: could not save game\n"

def cmd_load(args):
    global b
    if len(args) != 1:
        return "load: invalid usage: see help\n"
    else:
        try:
            with open(args[0], "r") as f:
                b = Board.deserialize(f.read())
        except Exception as e:
            return "load: could not load game\n"

def cmd_help(args):
    return (
        ("help: invalid usage\n" if len(args) != 0 else "") +
        "Valid commands are:\n\n"
        "  move [src] to [dest]\n"
        "    - move cards on the board\n"
        "  auto\n"
        "    - automatically move cards into the foundation zone\n"
        "  draw\n"
        "    - draw the next card from the deck\n"
        "  exit or quit\n"
        "    - end the game\n"
        "  restart\n"
        "    - restart the game\n"
        "  save [file]\n"
        "    - save progress into [file]\n"
        "  load [file]\n"
        "    - load progress from [file]\n"
        "  help\n"
        "    - show this help\n\n"
        "src and dest can be any of the following:\n"
        "  - drop           .. the drop zone\n"
        "  - foundation     .. the foundation zone\n"
        "  - [suit]         .. the top card of the [suit] foundation zone\n"
        "  - [number]       .. the stack labeled [number]\n"
    )

def parse_cmd():
    choice = input("> ")
    args = choice.split(" ")
    if len(args) == 1 and args[0] == "":
        return True

    cmd, *args = args
    if cmd not in commands:
        print("{}: not a valid command: see help".format(cmd))
        return False
    else:
        res = commands[cmd](args)
        if res != None:
            print(res, end = "")
            return False
        else:
            return True

commands = {
    "move": cmd_move,
    "mv": cmd_move,
    "m": cmd_move,

    "auto": cmd_auto,
    "a": cmd_auto,

    "draw": cmd_draw,
    "d": cmd_draw,

    "exit": cmd_exit,
    "e": cmd_exit,

    "quit": cmd_exit,
    "q": cmd_exit,

    "restart": cmd_restart,
    "r": cmd_restart,

    "save": cmd_save,
    "s": cmd_save,

    "load": cmd_load,
    "l": cmd_load,

    "help": cmd_help,
    "h": cmd_help,
    "?": cmd_help
}

def redraw():
    print("\033[1J\033[0;0H", end = "")
    print(b.display())

def autosave_name():
    savefile = "/tmp/tmp.soliterm"
    if "USER" in os.environ:
        savefile += "." + os.environ["USER"]
    savefile += ".save"
    return savefile

def check_autosave():
    savefile = autosave_name()
    if os.path.isfile(savefile):
        ans = None
        while ans != "" and ans != "y" and ans != "n":
            ans = input("Automatic save file found, load it? [Y/n] ").lower()

        if ans == "" or ans == "y":
            cmd_load([savefile])

def remove_autosave():
    savefile = autosave_name()
    if os.path.isfile(savefile):
        os.remove(savefile)

def main():
    try:
        check_autosave()
        while not b.game_won():
            redraw()
            while not parse_cmd():
                pass
            cmd_save([autosave_name()])
            print()
        print("Congratulations, you won!")
    except EOFError:
        pass

    remove_autosave()

if __name__ == "__main__":
    main()
