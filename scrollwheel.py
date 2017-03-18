#!/usr/bin/env python

#  ccw: ??01004f1000
#   cw: ??ff004f1000
# down: 01??004f1000
#   up: 00??004f1000

def daemonize():
    import os
    pid = os.fork()
    if pid != 0:
        print pid
        return True
    else:
        os.setsid()

    return False

class CSVOutputDriver:
    def __init__(self, outport, multiplier=None):
        self.outport = open(outport, "ab")

    def scroll(self, delta, pressed):
        self.outport.write("%i,%s\r\n" % (delta, pressed))
        self.outport.flush()


class MouseOutputDriver:
    def __init__(self, outport, multiplier=32):
        import os
        if not os.path.exists(outport):
            os.mkfifo(outport, 0600)

        self.outport = open(outport, "ab")
        self.multiplier = multiplier

    def scroll(self, delta, pressed):
        if delta == 0:
            return

        if pressed:
            delta *= self.multiplier
            if delta < -128:
                delta = -128
            elif delta > 127:
                delta = 127

        if delta == 0:
            b6 = 0
            b7 = 0
        elif delta > 0:
            if delta < 0x40:
                b6 = delta
                b7 = 0
            else:
                b6 = 0x3f
                b7 = delta - 0x3f
        elif delta < 0:
            if delta < -0x40:
                b6 = -0x40
                b7 = delta + 0x40
            else:
                b6 = delta
                b7 = 0
                    
        if b6 != 0 or b7 != 0:
            if b6 < 0:
                b6 += 0x80
            if b7 < 0:
                b7 += 0x80
            self.outport.write("\x87\x00\x00\x00\x00%s%s\x7f" % (chr(b6), chr(b7)))
            self.outport.flush() 

class KeyboardOutputDriver:
    def __init__(self, outport=None, multiplier=None):
        from xdo import Xdo, CURRENTWINDOW
        self.xdo = Xdo()
        self.CURRENTWINDOW = CURRENTWINDOW

    def sendkey(self, keysym):
        self.xdo.send_keysequence_window(self.CURRENTWINDOW, keysym)

    def scroll(self, delta, pressed):
        keysym = None

        if delta < 0:
            keysym = "Page_Up"   if pressed else "Up"
        elif delta > 0:
            keysym = "Page_Down" if pressed else "Down"

        if keysym is not None:
            for i in range(abs(delta)):
                self.sendkey(keysym)


class WheelInputDriver:
    def __init__(self, inport):
        self.inport = inport
        self.inport.write("\x00")

    def get_event(self):
        event = self.inport.read(6)
        if event.endswith("\x10\x00"):
            pressed =   ord(event[0]) > 0
            delta   = ((ord(event[1]) + 128) % 256) - 128
            led     =   ord(event[3])
            return pressed, delta, led
        else:
            return 0, 0

    def set_led(self, light):
        self.inport.write(chr(int(((float(light) / 2) ** 2) * 255)))




def main():
    import os
    from sys import argv, stdin, stdout, stderr
    import argparse

    parser = argparse.ArgumentParser(description='Driver for Griffin PowerMate')
    parser.add_argument('-d', '--driver',     nargs='?', choices=['mouse', 'keyboard', 'csv'], dest='driver',               default='mouse',       help='Output driver: mouse generates scroll events; keyboard generates key presses; csv generates CSV output to specified mouse_device path.')
    parser.add_argument('-i', '--input',      nargs='?', metavar='wheel_device',               dest='inport',               default='/dev/uhid0',  help='The Griffin PowerMate device node. Defaults to "/dev/uhid0".')
    parser.add_argument('-o', '--output',     nargs='?', metavar='mouse_device',               dest='outport',              default='/dev/stdout', help='The mouse device node. The default is stdout, and is for piping into `moused -f -p /dev/stdin -t sysmouse -d -d`. If a non-existent path is specified then it is created as a fifo.')
    parser.add_argument('-m', '--multiplier', nargs='?', metavar='multiplier',                 dest='multiplier', type=int, default=32,            help='Multiplier to apply to mouse scroll events when the scroll wheel is pressed.')
    parser.add_argument('-v', '--verbose',                                                     dest='debug',     action='store_true')
    parser.add_argument('-f', '--foreground',                                                  dest='daemonize', action='store_false')


    args = parser.parse_args()

    if args.daemonize:
        if daemonize():
            return

    wheel = WheelInputDriver(open(args.inport, "a+b"))

    scroller = {
        "mouse": MouseOutputDriver,
        "keyboard": KeyboardOutputDriver,
        "csv":      CSVOutputDriver,
    }[args.driver](args.outport, args.multiplier)

    while True:
        pressed, delta, led = wheel.get_event()
        if args.debug:
            stderr.write("%s,%i,%i\r\n" % (pressed, delta, led))
            stderr.flush()

        light = 0

        if pressed:
            light += 1

        if delta != 0:
            light += 1

        wheel.set_led(light)

        scroller.scroll(delta, pressed)

        if delta != 0:
            light -= 1

        wheel.set_led(light)

                
if __name__ == '__main__':
        main()
