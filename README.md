# powermate
Generic USB Driver for Griffin PowerMate

Supports three types of outputs:
1. Mouse protocol scroll events, for `moused` hacked to avoid errors relating to missing ioctls.
2. X11 keyboard events using Xdo, sending `Up`, `Down`, `Page_Up`, `Page_Down` keysyms.
3. Text CSV records, for debugging, or whatever else you want.

See `./scrollwheel.py -h` for usage information.
