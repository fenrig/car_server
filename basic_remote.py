#!/usr/bin/python3
#####################################
# Author: Matthias Van Gestel
#####################################
# --- Guides ---
# * http://www.doughellmann.com/PyMOTW/socket/tcp.html
# * http://docs.python.org/2/library/socket.html#socket.socket.listen
# * http://docs.python.org/3.3/howto/sockets.html#socket-howto
#####################################
'''
Nog niet uitgewerkt en is redelijk ruw
'''
import socket
import sys
import threading
import time

# TCP/IP Socket aanmaken
sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbind de socket met de poort waarop de server luisterd
server_address = (socket.gethostname(), 666)
sys.stderr.write("[INFO] Connecting to '%s' port '%s'\n" % server_address)
sockobject.connect(server_address)

# Authenticatie
clienttype = "basic_remote"
sockobject.sendall(bytes(clienttype, 'UTF-8'))
sys.stderr.write("[INFO] Authenticate as: '%s'\n" % clienttype)

# Choose car
sys.stderr.write("[INFO] Choose Car\n")
quantity = int(sockobject.recv(6))
for i in range(quantity):
	data = sockobject.recv(12)
	sys.stderr.write("[INFO] Received: '%s'\n" % data)
sockobject.sendall(data)
sys.stderr.write("[INFO] Sending: '%s'\n" % data)

def recv():
	while True:
		# Luisteren voor een antwoord
		'''
		amount_received = 0
		amount_expected = len(message)
		while amount_received < amount_expected:
		'''
		data = sockobject.recv(56)
		sys.stderr.write("[INFO] Received: '%s'\n" % data)
		if data == bytes("", 'UTF-8'): # Var gebruiken ipv bytes()
			sys.stderr.write("[ERROR] No more data")
			exit()
			break

def send():
	while True:
		# Verstuur data
		# Voorlopige test code
		message = 'forward'
		sys.stderr.write("[INFO] Sending: '%s'\n" % message)
		sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
		time.sleep(2)
		message = 'forward'
		sys.stderr.write("[INFO] Sending: '%s'\n" % message)
		sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
		time.sleep(2)
		message = 'backward'
		sys.stderr.write("[INFO] Sending: '%s'\n" % message)
		sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
		time.sleep(2)

transmit = threading.Thread(target=send)
transmit.start()
receive = threading.Thread(target=recv)
receive.start()

while True:
	i = 0
	i = i + 1
	if i > 300:
		i = i - 500
	time.sleep(100)