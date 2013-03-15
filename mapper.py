#!/usr/bin/python3
#####################################
# Author: Matthias Van Gestel
#####################################
# Overloading constructor: http://stackoverflow.com/questions/141545/overloading-init-in-python
#####################################
import time
# drawing on canvas
import tkinter as tk
import copy
# xml
import xml.etree.ElementTree as etree

###############XML#########################
def get_location(element):
	x = int(element.find("x").text)
	y = int(element.find("y").text)
	return (x,y)

def parse_connection(element):
	No_Connection = (None,None)
	if element is None: 
		element = No_Connection
	else:
		element = get_location(element)
	return element


def parse_mapping_xml():
	tree = etree.parse('map.xml')
	root = tree.getroot()

	map = []

	for child in root:
		name = child.find("name").text
		if name is None: continue

		xy   = get_location(child)
		if xy is (None,None): continue

		n    = child.find("n")
		o 	 = child.find("o")
		s    = child.find("s")
		w    = child.find("w")

		n    = parse_connection(n)
		o    = parse_connection(o)
		s    = parse_connection(s)
		w    = parse_connection(w)

		node = mapping_node(name,xy,(n,o,s,w))
		map.append(node)

	return map


###############CANVAS######################
size = 50
line_width = 10

width  = 800
height = 800

def convert_coordinates(location):
	coordinates = copy.deepcopy(location)
	x = (coordinates.x * size) + (width  / 2)
	y = (coordinates.y * size) + (height / 2)
	return x,y


def canvas(map):
	master = tk.Tk()
	canv = tk.Canvas(master,width = width,height = height)
	canv.pack()
	for element in map:
		x,y = convert_coordinates(element.loc)
		canv.create_rectangle(x,y, (x+size), (y+size), fill = "red")
		canv.create_text(x + 10,y + 10, text = element.name)
		if element.connections.o.is_empty() is False:
			x2,y2 = convert_coordinates(element.connections.o)
			canv.create_line(x+size+1,y+10,x2,y2+10, fill="yellow", width = line_width)
		if element.connections.w.is_empty() is False:
			x2,y2 = convert_coordinates(element.connections.w)
			canv.create_line(x,y+size-10,x2+size+1,y2+size-10, fill="orange", width = line_width)
		if element.connections.n.is_empty() is False:
			x2,y2 = convert_coordinates(element.connections.n)
			canv.create_line(x+10,y,x2+10,y2+size+1, fill="blue", width = line_width)
		if element.connections.s.is_empty() is False:
			x2,y2 = convert_coordinates(element.connections.s)
			canv.create_line(x+size-10,y+size+1,x2+size-10,y2, fill="purple", width = line_width)
	tk.mainloop()

###############MAPPINGDATA##########################
# DATATYPES -> CLASSES

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

#############################MAIN#######################
if __name__=='__main__':
	map = parse_mapping_xml()
	canvas(map)
	