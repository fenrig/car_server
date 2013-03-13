#!/usr/bin/python3
#####################################
# Author: Matthias Van Gestel
#####################################
# Overloading constructor: http://stackoverflow.com/questions/141545/overloading-init-in-python
#####################################
import time
# drawing on canvas
from tkinter import *
import copy

size = 50
line_width = 10

def canvas(map):
	master = Tk()
	width  = 800
	height = 800
	canv = Canvas(master,width = width,height = height)
	canv.pack()
	for element in map:
		coordinates = copy.deepcopy(element.loc)
		x = (coordinates.x * size) + (width  / 2)
		y = (coordinates.y * size) + (height / 2)
		canv.create_rectangle(x,y, (x+size), (y+size), fill = "red")
		canv.create_text(x + 10,y + 10, text = element.name)
		if element.connections.o.is_empty() is False:
			coordinates2 = copy.deepcopy(element.connections.o)
			x2 = (coordinates2.x * size) + (width / 2)
			y2 = (coordinates2.y * size) + (height / 2)
			canv.create_line(x+size+1,y+10,x2,y2+10, fill="yellow", width = line_width)
		if element.connections.w.is_empty() is False:
			coordinates2 = copy.deepcopy(element.connections.w)
			x2 = (coordinates2.x * size) + (width / 2)
			y2 = (coordinates2.y * size) + (height / 2)
			canv.create_line(x,y+size-10,x2+size+1,y2+size-10, fill="orange", width = line_width)
		if element.connections.n.is_empty() is False:
			coordinates2 = copy.deepcopy(element.connections.n)
			x2 = (coordinates2.x * size) + (width / 2)
			y2 = (coordinates2.y * size) + (height / 2)
			canv.create_line(x+10,y,x2+10,y2+size+1, fill="blue", width = line_width)
		if element.connections.s.is_empty() is False:
			coordinates2 = copy.deepcopy(element.connections.s)
			x2 = (coordinates2.x * size) + (width / 2)
			y2 = (coordinates2.y * size) + (height / 2)
			canv.create_line(x+size-10,y+size+1,x2+size-10,y2, fill="purple", width = line_width)
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
		self.n = location(n[0],n[1])
		self.o = location(o[0],o[1])
		self.s = location(s[0],s[1])
		self.w = location(w[0],w[1])

class mapping_node(object):
	'''
	Node
	'''
	def __init__(self, strname, xy, nosw):
		self.name = strname
		self.loc = location(xy[0],xy[1])
		self.connections = node_connections(nosw[0],nosw[1],nosw[2],nosw[3])	

if __name__=='__main__':
	map = []
	map.append( mapping_node("A",(0,0),((None,None),(3,0),(0,3),(None,None))) )
	map.append( mapping_node("B",(3,0),((None,None),(None,None),(3,3),(map[0].loc.x, map[0].loc.y))) )
	map.append( mapping_node("C",(0,3),((map[0].loc.x, map[0].loc.y),(3,3),(None,None),(None,None))))
	map.append( mapping_node("D",(3,3),((map[1].loc.x, map[1].loc.y),(None,None),(None,None),(map[2].loc.x, map[2].loc.y))) )
	canvas(map)
	