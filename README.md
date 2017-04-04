# powermate
Generic USB Driver for Griffin PowerMate

Supports 4 output drivers: 
1. `moused`: "sysmouse" protocol scroll events, for piping into `moused`.
2. `xmouse`: X11 mouse scroll events using Xdo.
3. `xkeyboard`: X11 keyboard events using Xdo, sending `Up`, `Down`, `Page_Up`, `Page_Down` keysyms.
4. `csv`: Text CSV records, for debugging, or whatever else you want.

See `./scrollwheel.py -h` for usage information.
