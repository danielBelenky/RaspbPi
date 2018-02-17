#!/usr/bin/env python3
#
# Simple FAN controller for Raspberry PI
#
# WARNING! It is NOT recommended to plug the fan directly to GPIO pins. You may
# damage your board. The best solution is to attach a transistor to one of the
# GPIO pins and signal through it.
#

import signal
from subprocess import check_output
from time import sleep
from RPi import GPIO


PIN = 18
# Temp is in C
MAX_TEMP = 55


def main():
    signal.signal(signal.SIGINT, clean)
    cooling = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    while True:
        if get_cpu_temp() >= MAX_TEMP and not cooling:
            cool_rpi()
            cooling = True
        elif cooling:
            cool_enough()
            cooling = False
        sleep(5)


def clean(signum, frame):
    GPIO.cleanup()


def cool_rpi():
    GPIO.output(PIN, True)
    COOLING = True


def cool_enough():
    GPIO.output(PIN, False)
    COOLING = False


def get_cpu_temp():
    temp = float(check_output(["vcgencmd", "measure_temp"])[5:-3])
    print('Temp is {0}'.format(temp))
    return temp


if __name__ == "__main__":
    main()
