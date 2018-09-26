import serial
import time

s = None


def setup():
    # open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1)
    # the baudrate is set to 57600 and should be the same as the one
    # specified in the Arduino sketch uploaded to ATMega32U4.
    global s
    s = serial.Serial("/dev/ttyS0", 57600)


def loop():
    flex = s.readline()
    if int(flex) >= 500:
        s.write("1")
    else:
        s.write("0")
    print(flex)


if __name__ == '__main__':
    setup()
    print("working!")
    while True:
        loop()
