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
import pygame
from pygame.locals import *

# TCP/IP Socket aanmaken
sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbind de socket met de poort waarop de server luisterd
server_address = (socket.gethostname(), 666)
sys.stderr.write("[INFO] Connecting to '%s' port '%s'\n" % server_address)
sockobject.connect(server_address)

# Authenticatie
clienttype = "basic_remote"
sockobject.sendall(clienttype)
sys.stderr.write("[INFO] Authenticate as: '%s'\n" % clienttype)

# Choose car
sys.stderr.write("[INFO] Choose Car\n")
sockobject.sendall("get_clients".ljust(56))
data = sockobject.recv(56).decode("utf-8").strip()
sys.stderr.write("[INFO] Received: '%s'\n" % data)

listn = data.split(";")
sockobject.sendall('set_car'.ljust(56))
sockobject.sendall(listn[0].ljust(56))
sys.stderr.write("[INFO] Sending: '%s'\n" % listn[0])

#------- pygame part
width_height = (802, 802)
pygame.init()
DISPLAYSURF = pygame.display.set_mode(width_height)
pygame.display.set_caption("Matthias Van Gestel - Computernetwerken Game")
# ------
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
        if data.strip() == "": # Var gebruiken ipv bytes()
            sys.stderr.write("[ERROR] No more data")
            sys.exit()
            break

def send():
    while True:
        # Verstuur data
        # Voorlopige test code
        '''
        message = 'forward'
        sys.stderr.write("[INFO] Sending: '%s'\n" % message)
        sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
        time.sleep(10)
        message = 'left'
        sys.stderr.write("[INFO] Sending: '%s'\n" % message)
        sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
        time.sleep(10)
        message = 'backward'
        sys.stderr.write("[INFO] Sending: '%s'\n" % message)
        sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
        time.sleep(10)
        message = 'right'
        sys.stderr.write("[INFO] Sending: '%s'\n" % message)
        sockobject.sendall(bytes(message.ljust(56), 'UTF-8'))
        time.sleep(10)
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    message = 'forward'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))
                if event.key == K_DOWN:
                    message = 'backward'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))
                if event.key == K_LEFT:
                    message = 'left'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))
                if event.key == K_RIGHT:
                    message = 'right'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))
            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    message = 'fb-stop'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))
                if event.key == K_LEFT or event.key == K_RIGHT:
                    message = 'lr-stop'
                    sys.stderr.write("[INFO] Sending: '%s'\n" % message)
                    sockobject.sendall(message.ljust(56))

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