#!/usr/bin/python3
#####################################
# Author: Matthias Van Gestel
#####################################
# --- Guides ---
# * http://www.doughellmann.com/PyMOTW/socket/tcp.html
# * http://docs.python.org/2/library/socket.html#socket.socket.listen
# * http://docs.python.org/3.3/howto/sockets.html#socket-howto
# * http://stackoverflow.com/questions/487229/client-server-programming-in-python
# * http://stackoverflow.com/questions/2905965/creating-threads-in-python
# * http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies
# * http://www.devshed.com/c/a/Python/Sockets-in-Python-Into-the-World-of-Python-Network-Programming/3/
# * https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/Multithreading/CreatingThreads/CreatingThreads.html
# * http://www.ibm.com/developerworks/linux/tutorials/l-pysocks/section4.html
# * http://www.doughellmann.com/PyMOTW/abc/
# * http://code.activestate.com/recipes/577278-receive-udp-broadcasts/
# * d
#####################################
# TODO: objecten gebruiken voor interthreaded communicatie (fancy)
#       http://docs.python.org/3.3/tutorial/classes.html
#       [ DONE ]
# TODO: verbeteren van client server states zodat bovenstaande
#       TODO kan afgewerkt worden
#       [ DONE ]
# TODO: Classes opschonen, mogelijk maken van remote en car object
#       [ DONE ]
# TODO: Eigen protocol produceren
#       [ PARTIALLY ]
#           * Authenticatie protocol
#           * Basic remote protocol
#               [ ALMOST DONE ]
#           * Basic car_v1 protocol
#               [ ALMOST DONE ]
# TODO: } van de vorige --> Afstandbediening moet auto kunnen aansturen
#####################################

import socket
import select
import sys
import threading
import time
import abc

import mapper

#----------------------------------------------------------


def identify(identifier, mapobject, clients):
    '''
    Returned het bijhorende object bij een type die hoort bij een
    bepaalde bytes(string) [12 bytes -> 12 char]
    '''
    if identifier == bytes("car_v2      ", 'UTF-8'):
        return car_v2(mapobject)
    if identifier == bytes("car_v1      ", 'UTF-8'):
        return car_v1()
    if identifier == bytes("basic_remote", 'UTF-8'):
        return basic_remote()
    if identifier == bytes("advan_remote", 'UTF-8'):
        return advanced_remote(mapobject, clients)
    return False


class client_base(object):
    __metaclass__ = abc.ABCMeta

    counter = 0

    def __init__(self):
        '''
        Constructor
        '''
        self.name = "client %i" % self.counter
        self.counter = self.counter + 1
        self.string_messages = []

    def send(self, message):
        '''
        Bericht buffer vullen
        [ Buffer kan momenteel maar 1 bericht vasthouden ]
        '''
        self.string_messages.append(message)

    def message(self):
        if not self.string_messages:
            return False
        return True

    def sent(self):
        '''
        Bericht verstuurd dus (mini) buffer leeg maken
        [ Buffer kan momenteel maar 1 bericht vasthouden ]
        '''
        return self.string_messages.pop(0)

    def getname(self):
        return self.name

    def clientdisconnected(self):
        '''
        class counter decreasen (niet belangrijk)
        '''
        self.counter = self.counter - 1

    @abc.abstractmethod
    def gettype(self):
        '''
        Zo kan er gecontroleerd worden van welk type
        een object is
        '''
        pass

    @abc.abstractmethod
    def decode_instruction(self, instruction):
        '''
        Decodeerd een instructie van 56 bytes --> 56 char
        en voert de instructie uit
        '''
        pass


class basic_remote(client_base):
    '''
    Afstandbediening (basic version)
    '''
    def __init__(self):
        # Constructor base class callen
        client_base.__init__(self)
        # Derived class constructen
        self.name = "basic_remote %i" % self.counter

    def set_clientobject(self, clientobjectx):
        # Clientobject (te besturen client) instellen
        self.clientobject = clientobjectx

    def gettype(self):
        return "basic_remote"

    def decode_instruction(self, instruction):
        # TODO: Afwerken eenmaals car_v1 "werkt"
        if instruction == "forward":
            self.clientobject.forward()
            return
        if instruction == "backward":
            self.clientobject.backward()
            return
        if instruction == "horizontal_stop":
            sys.stderr.write(str(instruction) + "\n")
            return
        if instruction == "left":
            self.clientobject.left()
            return
        if instruction == "right":
            self.clientobject.right()
            return
        if instruction == "vertical_stop":
            sys.stderr.write(str(instruction) + "\n")
            return

    def send_clients(self, clientsock, clients):
        '''
        Aantal clienten (6 bytes) in UTF-8
        +
        Namen van Bestuurbare clients  (12 bytes per client)
        Versturen
        ---------------
        [6 bytes][12 bytes][12 bytes] ... [12 bytes]
        'Aantal'  'Client name'
        '''
        counter = 0
        # Aantal tellen en versturen in 12 bytes
        for clientobject in clients:
            if clientobject.gettype() == "car_v1":
                counter = counter + 1
        quantity = str("%06d" % counter)
        clientsock.sendall(bytes(quantity, 'UTF-8'))
        sys.stderr.write("[INFO] Sending: '%s'\n" % quantity)
        # Client names versturen
        for clientobject in clients:
            if clientobject.gettype() == "car_v1":
                client = clientobject.getname()
                client = client.ljust(12)
                clientsock.sendall(bytes(client, 'UTF-8'))
                sys.stderr.write("[INFO] Sending: '%s'\n" % client)

    def get_client(self, clientsock, clients):
        '''
        Client instellen (eerder de procedure)
        [ 12 bytes ]
        '''
        sys.stderr.write("[INFO] Receiving remote clientobject\n")
        rlist, wlist, elist = select.select([clientsock], [], [], 1)
        while [rlist, wlist, elist] == [[], [], []]:
            time.sleep(1)
        receive_bytes = clientsock.recv(12)
        sys.stderr.write("[INFO] Received: '%s'\n" % receive_bytes)
        for clientobject in clients:
            if receive_bytes == bytes(clientobject.getname().ljust(12), 'UTF-8'):
                print("Set")
                self.set_clientobject(clientobject)
                return


class car_v1(client_base):
    '''
    Basic voertuig
    '''
    # TODO: afwerken
    def __init__(self):
        client_base.__init__(self)
        self.name = "car_v1 %i" % self.counter

    def gettype(self):
        return "car_v1"

    def decode_instruction(self, instruction):
        if instruction == "5m":
            print(instruction)

    def forward(self):
        self.send("forward")
        
    def backward(self):
        self.send("backward")

    def fbstop(self):
        self.send("fb-stop")

    def left(self):
        self.send("left")

    def right(self):
        self.send("right")


class advanced_remote(client_base):
    '''
    Advanced Remote
    '''
    def __init__(self, mabobject, clients):
        client_base.__init__(self)
        self.name = "advanced_remote %i" % self.counter
        self.mapobject = mapobject
        self.clients = clients
        self.flags = 0
        self.controlled_car = None

    def gettype(self):
        return "advanced_remote"

    def decode_instruction(self, instruction):
        if self.flags == 1:
            self.flags = 0
            for client in self.clients:
                if type(client) == car_v2:
                    if client.name == instruction:
                        if client.locked is False:
                            self.controlled_car = client
                            sys.stderr.write("[INFO] '%s' (advanced_remote) controls '%s'\n" % (self.name, client.name))
                            self.send("set_car succeeded")
                            return
                        else:
                            sys.stderr.write("[INFO] '%s' is locked\n" % (client.name))
                            self.send("set_car failed")
            sys.stderr.write("[INFO] '%s' (advanced_remote) cannot control '%s'\n" % (self.name, instruction))
            self.send("set_car failed")
        elif self.flags == 2:
            self.flags = 0
            for node in self.mapobject.raw_map:
                if node.name == instruction:
                    self.controlled_car.origin = node
                    self.send("set_origin succeeded")
                    return
            self.send("set_origin failed")
        elif self.flags == 3:
            self.flags = 0
            for node in self.mapobject.raw_map:
                if node.name == instruction:
                    self.controlled_car.destination = node
                    self.send("set_destination succeeded")
                    if self.controlled_car.origin is not None:
                        self.controlled_car.emitInstructionListChanged()
                    return
            self.send("set_destination failed")
        elif instruction == "getCar_V2":
            cars = []
            for client in self.clients:
                if type(client) == car_v2:
                    cars.append(client)
            if len(cars) == 0:
                string = "-"
            else:
                string = ""
                for car in cars:
                    string = string + car.name + ";"
            self.send(string)
        elif instruction == "set_car":
            self.flags = 1
        elif instruction == "get_nodes":
            if len(self.mapobject.raw_map) == 0:
                string = "-"
            else:
                string = ""
                for node in self.mapobject.raw_map:
                    string = string + node.name + ";"
            self.send(string)
        elif instruction == "set_origin":
            self.flags = 2
        elif instruction == "set_destination":
            self.flags = 3
        elif instruction == "lock":
            self.controlled_car.lock()


class car_v2(client_base):
    '''
    Advanced voertuig
    '''
    def __init__(self, mapobject):
        client_base.__init__(self)
        self.name = "car_v2 %i" % self.counter
        self.origin = None
        self.destination = None
        self.mapobject = mapobject
        self.locked = False
        # self.origin = mapobject.raw_map[0]
        # self.destination = mapobject.raw_map[5]
        # self.emitInstructionListChanged()

    def gettype(self):
        return "car_v2"

    def decode_instruction(self, instruction):
        if instruction == "5m":
            print(instruction)
        if instruction == "get_instructions":
            instructions = self.mapobject.instr_list(self.origin, self.destination)
            #self.send("instructions: " + str(len(instructions)))
            string = ""
            for instruction in instructions:
                string = string + str(instruction[0]) + ";"
            #self.send(string)
            self.send("n;s;n;w;n;e;s;w;e;w;s;e;n")
            return
        print("Failed parsing")

    def emitInstructionListChanged(self):
        self.send("instructionlist_changed")

    def lock(self):
        if self.locked is False:
            self.locked = True
        else:
            self.locked = False


#----------------------------------------------------------
def client_handler(clientsock, client_address, clients, mapobject):
    '''
    Client thread (momenteel universeel)
    '''
    try:
        # om nog gebruik te kunnen maken van de "lelijke" try ... finally (return's triggeren finally)
        flag_except = True
        sys.stderr.write("[INFO] Connection with '%s' on '%s'\n" % client_address)
        # Authenticatie gedeelte [12 bytes]
        receive_bytes = clientsock.recv(12)
        clientobject = identify(receive_bytes, mapobject, clients)
        if clientobject is False:
            sys.stderr.write("[ERROR] Bad authentication with '%s:%s'\n" % client_address)
            flag_except = False
            return
        sys.stderr.write("[INFO] '%s' authenticated at '%s:%s'\n" % (clientobject.gettype(), client_address[0], client_address[1]))
        clients.append(clientobject)
# ------- deel maken van het object --> "basic remote"
        # Remote doen kiezen welke auto er bestuurd wordt
        if clientobject.gettype() == "advan_remote":
            clientobject.send_clients(clientsock, clients)
            clientobject.get_client(clientsock, clients)
# -------
        # Client loop
        while True:
            # Controleren op te verkrijgen bericht
            rlist, wlist, elist = select.select([clientsock], [], [], 1)
            if [rlist, wlist, elist] != [[], [], []]:
                # Bericht is beschikbaar dus bericht moet gelezen worden
                receive_bytes = clientsock.recv(56).decode("utf-8").strip()
                sys.stderr.write("[INFO] Received: '%s' from '%s:%s'\n" % (receive_bytes, client_address[0], client_address[1]))
                # "Lege data" --> dode socket
                #if receive_bytes == bytes("", 'UTF-8'): # Var gebruiken ipv bytes()
                if not receive_bytes:
                    sys.stderr.write("[ERROR] No more data from '%s:%s'\n" % client_address)
                    break
                # Bericht/Instructie decoden en behandelen
                clientobject.decode_instruction(receive_bytes)
            # Controleren of er een bericht moet gestuurd worden
            if clientobject.message():
                # Zoja bericht versturen
                transmit_bytes = clientobject.sent()
                sys.stderr.write("[INFO] Sending: '%s'\n" % transmit_bytes)
                clientsock.sendall(bytes(transmit_bytes.ljust(56), 'UTF-8'))

    finally:
        # Socket proper afsluiten en variablen doorheen het programma schoonmaken
        if flag_except is True:
            sys.stderr.write("[INFO] Close connection with client '%s:%s'\n" % client_address)
            clientobject.clientdisconnected()
            clients.remove(clientobject)
            clientsock.close()


#----------------------------------------------------------
def mainthread(threads, clients):
    '''
    mapobject = mapper.CarMapper()
    print(mapobject.raw_map[0].name + " --> " + mapobject.raw_map[6].name)
    for i in mapobject.instr_list(mapobject.raw_map[0],mapobject.raw_map[6]):
        print(i)
    mapper.canvas(mapobject.raw_map)
    '''
    '''
    prev = mapper.create_route_map(map[0] , map)

    print(map[0].name + " -> " + map[9].name + " : ")
    for x in mapper.create_route(map[0], map[9], prev):
        print(x.name)
    mapper.canvas(map)
    '''

    while True:
        # Test code. Hiervan moeten berichten worden naartoe ge-offload en ge-upload (56 bytes per bericht)
        '''
        for i in clients:
            i.send("macarana")
        time.sleep(2)
        for i in clients:
            i.send("lalalalalalal")
        '''
        time.sleep(2)


def udp_thread():
    sys.stderr.write("[INFO] UDP Thread Started\n")
    # UDP broadcast listener
    udp_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_listen_socket.bind(('<broadcast>', 667))
    udp_listen_socket.setblocking(0)
    # UDP answer socket
    udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ----
    sys.stderr.write("[INFO] UDP Thread Initiated\n")
    while True:
        result = select.select([udp_listen_socket], [], [])
        msg, addr = result[0][0].recvfrom(56)
        msg = msg.decode("utf-8").strip()
        sys.stderr.write("[INFO] UDP Data: %s from %s:%s\n" % (msg, addr[0], addr[1]))
        if msg == "DISCOVER-CAR-SERVER":
            sys.stderr.write("[INFO] UDP Discover from %s\n" % addr[0])
            udp_send_socket.sendto(bytes("DISCOVERED-CAR-SERVER", "UTF-8"), (addr[0], 6666))
            #Answer with connection


#----------------------------------------------------------
if __name__ == '__main__':
    # Threading list
    threads = []
    # Client list
    clients = []
    # Main Thread starten
    mthread = threading.Thread(target=mainthread, args=[threads, clients])
    mthread.start()
    # Mapper opstarten
    mapobject = mapper.CarMapper()
    # TCP/IP (server)socket aanmaken
    sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Socket binden aan poort
    server_address = ('', 666)
    sockobject.bind(server_address)
    sys.stderr.write("[INFO] Socket starting up on '%s' port '%s'\n" % server_address)
    # Luisteren voor inkomende connecties
    sockobject.listen(1)
    # UDP Discovery thread starten
    udpthread = threading.Thread(target=udp_thread, args=[])
    udpthread.start()
    while True:
        # Wachten op connectie
        sys.stderr.write("[INFO] Waiting for connection\n")
        connection, client_address = sockobject.accept()
        sys.stderr.write("[INFO] Establishing connection with '%s' on '%s'\n" % client_address)
        # Thread starten en aan een lijst toevoegen
        threads.append(threading.Thread(target=client_handler, args=[connection, client_address, clients, mapobject]))
        threads[len(threads) - 1].start()
