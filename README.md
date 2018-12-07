# Soliterm

Unicode Solitaire Game for the terminal, based on the Klondike solitaire game.

![soliterm screenshot](/screenshots/soliterm.png)

[ASCIICast](https://asciinema.org/a/Mlo5jnMGhEnEtpcwag3xHNuxu)

## Dependencies

This project needs `python-colorama` (see
[requirements.txt](/requirements.txt)) and a unicode-compatible terminal
emulator (to render the playing cards).

Both Python2 and Python3 are supported.

## Rendering

Most terminal emulators do not display the Unicode playing cards used by this
game correctly. Some terminal emulators that do display the cards don't render
them as double-width characters, or use an odd width that results in characters
not being an integer number of columns in width.

It is also recommended to play with a relatively high font size to make the
cards readable.

For an optimal experience the Konsole terminal emulator is recommended, since it
displays Unicode playing cards as double-width characters correctly and allows
easy zooming / changing of the font size.

## Rules

The game is based on [Klondike solitaire](https://en.wikipedia.org/wiki/Klondike_\(solitaire\)):

The goal is to built up the four foundations by suit in the top right corner
from Ace to King. Cards on the board can be moved together in stacks of
alternating colors and consecutive card values. An empty slot on the board may
only be filled with a King.

Cards from the deck are drawn one at a time, and there is not limit to the
amount of passes through the deck. The deck is not shuffled after cycling
through it.

Aces or the next-highest value of a suit can be moved to the foundation of the
appropriate suit. When needed, cards of a suit may be moved back onto the board
from the foundations.

## Commands

The game is controlled through simple commands:

- `move [src] to dest`, `move [src] [dest]`, `m [src] to [dest]`, or `m [src] [dest]`:
  move cards on the board, see below
- `draw` or `d`: Draws the next card from the deck
- `auto` or `a`: Automatically moves cards to the foundations from the current
  board
- `exit`, `quit`, `e`, or `q`: end the game
- `restart` or `r`: restart the game
- `save [file]` or `s [file]`: save current board state to `[file]`
- `load [file]` or `l [file]`: load board state from `[file]`
- `help`: show help

## Moving Cards

Cards can be moved using the `move` command. Source and Destination can be one
of the following:

- `drop` or `d`: the "drop zone", aka the last card drawn from the deck (src
  only)
- `foundation` or `f`: the four foundations (dest only, suit determined
  automatically)
- `[suit]`: the top card of the `[suit]` foundation zone (src only)
- `[number]`: the stack labeled `[number]` on the board, always moves the
  largest stack possible.

## Suits

The four suits can be named as follows:

- `hearts`, `heart` or `h`
- `clubs`. `club`, or `c`
- `diamonds`, `diamond`, or `dia` (`d` is already taken by `drop`)
- `spades`, `spade`, or `s`

## Saving and Loading

The `save` command saves the game state as JSON into a file in the current
directory (or a path supplied to the command).

The game is also automatically saved every move to
`/tmp/tmp.soliterm.$USER.save`, or `/tmp/tmp.soliterm.save` is `$USER` is not
set.
Automatic savefiles are automatically deleted when the game is closed via
`exit`, `quit`, end of file, or winning.

When an automatic savefile is found at startup, the game asks if it should be
loaded.
