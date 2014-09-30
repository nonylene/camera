#coding:utf-8

import serial
import time
import struct
import datetime

def main():
    cam = serial.Serial('/dev/ttyAMA0',38400,timeout=0.1)
    camset(cam)
    capture(cam)

def camset(cam):
    time.sleep(0.25)
    print(cam)
    # reset
    cam.write(b'\x56\x00\x26\x00')
    time.sleep(1.0)
    read(cam)
    print('finish setting...')

def capture(cam):
    # takepic
    cam.write(b'\x56\x00\x36\x01\x00')
    read(cam)
    time.sleep(2.0)
    # getsize
    cam.write(b'\x56\x00\x34\x01\x00')
    time.sleep(0.5)
    print('size')
    a = str()
    a = cam.readline()
    kh = int(a[len(a)-2])
    kl = int(a[len(a)-1])
    print(kh,kl)
    readpic(cam,kh,kl)
    cam.write(b'\x56\x00\x34\x01\x03')
    cam.close()

def readpic(cam,kh,kl):
    s = b'\x56\x00\x32\x0C\x00\x0A\x00\x00'
    u = b'\x00\x00'
    w = b'\x00\x0A'
    # address
    t =  bytes([0]) + bytes([0])
    # size
    hx = bytes([kh])
    lx = bytes([kl])
    v = hx + lx
    cam.write(s+t+u+v+w)
    binary = cam.readline()
    a = binary
    while a:
        time.sleep(0.05)
        a = cam.readline()
        binary = binary + a
    print('finish readline...')
    # modify binary
    binary = binary[binary.find(b'\xff\xd8'):binary.rfind(b'\xff\xd9')+2]
    # write jpg
    date = str(datetime.datetime.today().strftime('%y%m%d-%H%M%S'))
    f = open('pic/pic' + date + '.jpg', 'wb')
    for i in binary:
        f.write(struct.pack('B',i))
    f.close()
    print('ended!')

def read(cam):
    a = cam.readline()
    while a:
        print(a)
        time.sleep(0.1)
        a = cam.readline()

if __name__ == '__main__':
    main()
