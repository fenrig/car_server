#!/usr/bin/python3
#####################################
# Author: Matthias Van Gestel
#####################################
# Overloading constructor: http://stackoverflow.com/questions/141545/overloading-init-in-python
#####################################
import time
# drawing on canvas
from tkinter import *

def canvas(map):
	master = Tk()
	canv = Canvas(master, width = 400, height = 400)
	canv.pack()
	mainloop()

class location(object):
	'''
	x and y
	'''
	def __init__(self, x = None , y = None):
		if x is None:
			self.empty = True
		else:
			self.empty = False
			self.x = x
			self.y = y


	def make_empty(bool = True):
		self.empty = bool

	def is_empty(self):
		return self.empty


class node_connections(object):
	'''
	Connectoren naar nodes (aan de hand van de posities)
	in de 4 windrichtingen
	'''
	def __init__(self, n, o, s, w):
		self.n = location(n)
		self.o = location(o)
		self.s = location(s)
		self.w = location(w)

class mapping_node(object):
	'''
	Node
	'''
	def __init__(self, strname, xy, nosw):
		self.streetname = strname
		self.loc = location(xy[0],xy[1])
		self.connections = node_connections(nosw[0],nosw[1],nosw[2],nosw[3])	

if __name__=='__main__':
	map = []
	map.append( mapping_node("A",(0,0),((None),(None),(None),(3,0))) )
	map.append( mapping_node("B",(3,0),((None),map[0].loc,(None),())) )
	canvas(map)
	while True:
		time.sleep(1)