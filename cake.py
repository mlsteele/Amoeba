import numpy
import math
import time

class c_master:
	def __init__(self):
		self.bucket = []
		self.bucklen = 0
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		newnode = c_node(self, i_mass, i_pos, i_vel)
		self.register_obj(newnode)
		return newnode
	
	def make_spring(self, i_ma, i_mb, i_targl, i_springk):
		newspring = c_spring(self, i_ma, i_mb, i_targl, i_springk)
		self.register_obj(newspring)
		return newspring
	
	def register_obj(self, i_obj):
		self.bucket.append(i_obj)
		self.bucklen = len(self.bucket)
	
	def update(self):
		for i in range(0,self.bucklen):
			self.bucket[i].update()

class c_node:
	def __init__(self, i_master, i_mass, i_pos, i_vel):
		# note: not integer resistant
		self.master = i_master
		self.pos = i_pos
		self.vel = i_vel
		self.accel = numpy.zeros(2)
		self.mass = i_mass
	
	def push(self, force):
		self.accel += force/self.mass
	
	def update(self):
		self.vel += self.accel
		self.pos += self.vel
		self.accel = numpy.zeros(2)

class c_spring:
	def __init__(self, i_master, i_ma, i_mb, i_targl, i_springk):
		self.master = i_master
		self.ma = i_ma
		self.mb = i_mb
		self.targl = float(i_targl)
		self.springk = float(i_springk)
	
	def update(self):
		pass