#!/usr/bin/python3

import socket
import binascii
import socket
import struct
import sys

TCP_IP = '10.1.20.40'
TCP_PORT = 1337
BUFFER_SIZE = 1024


values = (0x0001, 0x0008, b'sartoris')
packer = struct.Struct('I I 8s')
packed_data = packer.pack(*values)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(packed_data)

print('sending "%s"' % binascii.hexlify(packed_data), values)

print("Message sent")
s.close()