#coding:utf-8

import serial
import time
import struct

def main():
    cam = serial.Serial('/dev/ttyAMA0',38400,timeout=0.1)
    camset(cam)
    capture(cam)

def camset(cam):
    time.sleep(0.25)
    print(cam)
    #reset
    cam.write(b'\x56\x00\x26\x00')
    time.sleep(2.5)
    read(cam)
    print("setting end...")

def capture(cam):
    #takepic
    cam.write(b'\x56\x00\x36\x01\x00')
    print("hoe")
    read(cam)
    time.sleep(4.0)
    #getsize
    cam.write(b'\x56\x00\x34\x01\x00')
    time.sleep(1.0)
    print("size")
    a = str()
    a = cam.readline()
    kh = int(a[len(a)-2])
    kl = int(a[len(a)-1])
    print(kh,kl)
    readpic(cam,kh,kl)
    cam.write(b'\x56\x00\x34\x01\x03')
    cam.close()

def readpic(cam,kh,kl):
    f = open('test.txt', "ab")
    s = b'\x56\x00\x32\x0C\x00\x0A\x00\x00'
    u = b'\x00\x00'
    w = b'\x00\x0A'
    #address
    t =  bytes([0]) + bytes([0])
    #size
    hx = bytes([kh])
    lx = bytes([kl])
    v = hx + lx
    print(v)
    cam.write(s+t+u+v+w)
    a = cam.readline()
    time.sleep(0.5)
    while a:
        for i in a:
            f.write(struct.pack('B',i))
        a = cam.readline()
        time.sleep(0.05)
    f.close()
    print("ended!")
    #open test.txt binary editor and FFD8~FFD9

def read(cam):
    a = cam.readline()
    while a:
        print(a)
        #print(a.decode("utf-8").strip())
        time.sleep(0.1)
        a = cam.readline()

if __name__ == '__main__':
    main()
