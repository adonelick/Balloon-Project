# Written by Andrew Donelick


import serial
import time


def main():

    ser = serial.Serial('COM11', 19200, timeout=1)
    proceed = raw_input('Restart TT4')
    time.sleep(0.5)
    stuff = ser.read(200)
    print stuff

    ser.write(b'\x1b\x1b\x1b')
    time.sleep(0.5)
    stuff = ser.read(200)
    print stuff

    proceed = True
    while (proceed):
        command = raw_input('TinyTrak 4 Command: ')
        if command == "QUIT":
            proceed = False

        command += '\r'
        ser.write(command)
        time.sleep(0.5)

        returnString = ""
        while ser.inWaiting():
            returnString += ser.read()
            time.sleep(0.001)
        print returnString

    ser.close()
    




if __name__ == '__main__':
    main()