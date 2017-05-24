#!/bin/sh
case $1 in
	start)
		python scrollwheel.py -i "/dev/`dmesg | grep '^uhid.*Griffin' | cut -d: -f1`" > scrollwheel.pid
		;;
	stop)
		kill `cat scrollwheel.pid`
		;;
	restart)
		./service.sh stop
		./service.sh start
esac
