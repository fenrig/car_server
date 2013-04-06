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

################# MAPPEROBJECT ####################	
class CarMapper:
	def __init__(self):
		self.raw_map = self.parse_mapping_xml()
		self.routemap = {}
		for node in self.raw_map:
			node_map = self.create_route_map(node)
			self.routemap[node] = node_map


	def instr_list(self, originNode, destNode):
		node_list = self.create_route(originNode, destNode)
		return self.conv_to_instruction_list(node_list)

	def get_location(self, element):
		x = int(element.find("x").text)
		y = int(element.find("y").text)
		return (x,y)

	def parse_connection(self, element):
		No_Connection = (None,None)
		if element is None: 
			element = No_Connection
		else:
			element = self.get_location(element)
		return element


	def parse_mapping_xml(self):
		tree = etree.parse('map.xml')
		root = tree.getroot()

		map = []

		for child in root:
			name = child.find("name").text
			if name is None: continue

			xy   = self.get_location(child)
			if xy is (None,None): continue

			n    = child.find("n")
			o 	 = child.find("o")
			s    = child.find("s")
			w    = child.find("w")

			n    = self.parse_connection(n)
			o    = self.parse_connection(o)
			s    = self.parse_connection(s)
			w    = self.parse_connection(w)

			node = mapping_node(name,xy,(n,o,s,w))
			map.append(node)

		return map

	#############################ROUTING####################
	def convert_map(self, map):
		distance_dict  = {}
		previous_dict  = {}
		unvisited_list = []
		for v in map:
			distance_dict[v] = float('inf')
			previous_dict[v] = None
			unvisited_list.append(v)
		return distance_dict, previous_dict, unvisited_list

	def neighbors(self, node):
		connection_list = []
		if node.connections.n.is_empty() is False:
			connection_list.append(node.connections.n)
		if node.connections.o.is_empty() is False:
			connection_list.append(node.connections.o)
		if node.connections.s.is_empty() is False:
			connection_list.append(node.connections.s)
		if node.connections.w.is_empty() is False:
			connection_list.append(node.connections.w)

		neighbor_list = []
		for nodex in self.raw_map:
			for conx in connection_list:
				if nodex.loc.x == conx.x and nodex.loc.y == conx.y:
					neighbor_list.append(nodex)
					break

		return neighbor_list

	def distance(self,nodeX,nodeY):
		xdiff = nodeX.loc.x - nodeY.loc.x
		if xdiff < 0: xdiff = xdiff * (-1)

		ydiff = nodeX.loc.y - nodeY.loc.y
		if ydiff < 0: ydiff = ydiff * (-1)

		return (xdiff + ydiff)

	def create_route_map(self,startnode):
		'''
		Creates shortest route maps
		-----------------------------
		based on Dijkstra's Algorithm
		'''
		dist, prev, unvisited = self.convert_map(self.raw_map)

		dist[startnode] = 0

		while unvisited:
			shortest_node = unvisited[0]
			for node in unvisited:
				if dist[node] < dist[shortest_node]:
					shortest_node = node

			unvisited.remove(shortest_node)

			for neighbor in self.neighbors(shortest_node):
				new_distance = dist[shortest_node] + self.distance(shortest_node,neighbor)
				if new_distance < dist[neighbor]:
					dist[neighbor] = new_distance
					prev[neighbor] = shortest_node
		
		return prev

	def create_route(self,start_node, dest_node):
		route_list = self.routemap[start_node]

		route = [dest_node]

		cur_node = dest_node
		while cur_node is not start_node:
			cur_node_x = route_list[cur_node]
			cur_node   = cur_node_x
			route.insert(0, cur_node)

		return route

	def nosw_map_converter(self, cur_node, neighbor_next_node):
		if neighbor_next_node:
			if not cur_node.connections.n.is_empty():
				if cur_node.connections.n.x == neighbor_next_node.loc.x:
					if cur_node.connections.n.y == neighbor_next_node.loc.y:
						return "north"
			if not cur_node.connections.o.is_empty():
				if cur_node.connections.o.x == neighbor_next_node.loc.x:
					if cur_node.connections.o.y == neighbor_next_node.loc.y:
						return "east"
			if not cur_node.connections.s.is_empty():
				if cur_node.connections.s.x == neighbor_next_node.loc.x:
					if cur_node.connections.s.y == neighbor_next_node.loc.y:
						return "south"
			if not cur_node.connections.w.is_empty():
				if cur_node.connections.w.x == neighbor_next_node.loc.x:
					if cur_node.connections.w.y == neighbor_next_node.loc.y:
						return "west"
		else:
			return "TODO: last instruction"
		return "TODO: Couldn't find location"

	def conv_to_instruction_list(self, route_map):
		instruction_list = []
		count = -1
		for cur_node in route_map:
			count = count + 1
		for i in range(0,count):
			instruction_list.append(
				self.nosw_map_converter(route_map[i], route_map[i+ 1])
				)
		return instruction_list

	'''
	#############################MAIN#######################
	if __name__=='__main__':
		map = parse_mapping_xml()

		prev = create_route_map(map[0] , map)

		print(map[0].name + " -> " + map[9].name + " : ")
		for x in create_route(map[0], map[9], prev):
			print(x.name)
		
		canvas(map)
	'''
