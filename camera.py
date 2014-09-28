#coding:utf-8

import serial
import time

def main():
    cam = serial.Serial('/dev/ttyAMA0',38400)
    set(cam)

def set(a):
    time.sleep(0.25)
    print(a)
    #reset
    a.write(b'\x56\x00\x26\x00')
    time.sleep(3.0)
    if a.readline():
        print(a.readline())
    print("setting end...")

if __name__ == '__main__':
    main()
