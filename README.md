# powermate
Generic USB Driver for Griffin PowerMate on X11

## Summary
This can drive your [Griffen PowerMate](https://www.amazon.com/Griffin-Technology-NA16029-Multimedia-Controller/dp/B003VWU2WA/) on Linux and BSD operating systems, or any system with X11 and generic USB device nodes.

Supports 4 output drivers: 
1. `moused`: "sysmouse" protocol scroll events, for piping into `moused`.
2. `xmouse`: X11 mouse scroll events using Xdo.
3. `xkeyboard`: X11 keyboard events using Xdo, sending `Up`, `Down`, `Page_Up`, `Page_Down` keysyms.
4. `csv`: Text CSV records, for debugging, or whatever else you want.

See `./scrollwheel.py -h` for usage information.

## Dependendies
1. [python](https://python.org/)
2. [python-libxdo](https://pypi.python.org/pypi/python-libxdo/)
3. [libxdo from xdotool](https://github.com/jordansissel/xdotool)
