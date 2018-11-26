# Soliterm

Unicode Solitaire Game for the terminal, based on the Klondike solitaire game.

![soliterm screenshot](/screenshots/soliterm.png)

## Dependencies

This project needs `python-colorama` (see [requirements.txt](/requirements.txt)),
Python 3.7 (for type hinting), and a unicode-compatible terminal emulator (to
render the playing cards).

Python 3.6 and lower support can be achieved by removing the type hints from the
code.

It is recommended to play with a relatively high font size to make the cards
readable.

## Documentation

See the `help` command in game. Most commands can also be shortened to their
initials, and the `to` in the `move` command can be omitted.
