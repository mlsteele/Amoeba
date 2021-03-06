"""
Miles Steele
2010

Amoeba Generator
-----------------
Generates an amoeba to be used with the Cake physics engine.
"""

import random
import numpy as n

import cake

class amoeba_control:
	def __init__(self):
		s = self
		s.left = False
		s.right = False
		s.up = False
		s.down = False
		s.poof = False
		s.stick = False
		s.fat = False

class amoeba:
	def __init__(self, master, center_coords=n.zeros(2)):
		self.master = master

		self.center_coords = center_coords
		self.circle_res = 16
		self.circle_radius = 100.
		
		self.node_mass = 1.0
		self.treading = 3
		self.treadk = 1000.
		self.tread_damp = 0.
		
		self.musclek = 1000.
		self.muscle_period = .4
		self.muscle_amp = 100.
		self.muscle_damp = 0.
		
		self.phase = 0.
		self.gofactor = 0.
		
		self.control = amoeba_control()
		
	def assemble(self):
		## unit circle generation
		self.circle = []
		for i in range(0,self.circle_res):
			posx = n.cos(i*2.0*n.pi/self.circle_res)
			posy = n.sin(i*2.0*n.pi/self.circle_res)
			# mass transform
			posx *= self.circle_radius
			posy *= self.circle_radius
			posx += self.center_coords[0]
			posy += self.center_coords[1]
			# node creation
			newnode = self.master.make_node(self.node_mass, n.array([posx, posy])) #FLAG!!!
			self.circle.append(newnode)
		
		## tread generator
		self.tread = []
		for r in range(1,self.treading+1):
			for i in range(0,self.circle_res):
				length = n.linalg.norm(self.circle[i].pos - self.circle[i-r].pos)
				self.tread.append( self.master.make_spring(self.circle[i], self.circle[i-r], float(length), self.treadk, damp=self.tread_damp) )
		
		## muscle generator
		self.muscle_count = self.circle_res/2
		self.muscles = []
		self.muscle_length = self.circle_radius*2
		#muscle_length = n.linalg.norm(circle[i].pos - circle[i-4].pos) # should be at least close
		for i in range(0,self.muscle_count):
			self.muscles.append( self.master.make_spring(self.circle[i], self.circle[i-self.muscle_count], self.circle_radius*2, self.musclek, damp=self.muscle_damp) )
	
	def destroy(self):
		s = self
		
		for node in s.circle:
			s.master.nodes.remove(node)
			s.master.nodesLen -= 1
		
		for spring in s.tread:
			s.master.springs.remove(spring)
			s.master.springsLen -= 1
		
		for muscle in s.muscles:
			s.master.springs.remove(muscle)
			s.master.springsLen -= 1
	
	def update(self, timestep):
		s = self
		
		# Find Centroid
		centroid = n.zeros(2)
		for node in s.circle:
			centroid += node.pos
		centroid /= s.circle_res
		
		# Contact Test
		contact = False
		for node in s.circle:
			if node.contact:
				contact = True
		
		# Control
		for node in s.circle:
			rod = node.pos - centroid
			angle = n.arctan2(rod[1], rod[0])
			if s.control.left:
				if contact:
					node.accel -= 280 * n.array([ n.cos(angle + n.pi/2), n.sin(angle + n.pi/2) ])
				node.accel += [-60., 0.]
			if s.control.right:
				if contact:
					node.accel += 280 * n.array([ n.cos(angle + n.pi/2), n.sin(angle + n.pi/2) ])
				node.accel += [60., 0.]
			if s.control.up:
				node.accel += [0., -60.]
			if s.control.down:
				node.accel += [0., 60.]
			if s.control.fat:
				node.accel += [0., 300.]
			if (s.control.stick) & (node.contact):
				node.vel *= 0.
				node.accel *= 0.
		
		for muscle in s.muscles:
			muscle.springk = 20
			if s.control.poof:
				muscle.springk = 400
			if s.control.fat:
				muscle.springk = 400
	
	## UNSTABLE
	def updateSmart(self, timestep):
		# how are my feet feeling?
		touch = 0.
		for i in range(0, self.circle_res):
			if self.circle[i].contact:
				touch += 1.
		touchr = touch/self.circle_res
		
#		if (touchr) >= (1./4):
#			self.gofactor += 1.*timestep
#		elif (touch) >= 3:
#			pass
#		else:
#			self.gofactor -= .1*timestep
#			self.gofactor = max(self.gofactor, 0.)
		
		if touch >= 1.:
			self.gofactor += .05*timestep
		else:
			self.gofactor -= .1*timestep
		self.gofactor = min(self.gofactor, 1.)
		self.gofactor = max(self.gofactor, 0.)
		
		# update phase
		self.phase += timestep*self.gofactor
		self.phase = self.phase % self.muscle_period
		
		# run muscles
		for m in range(0,self.muscle_count):
			self.muscles[m].targl = self.muscle_amp * n.sin( (self.phase/self.muscle_period*2*n.pi) + (float(m)/self.muscle_count*2*n.pi) )
			self.muscles[m].targl += self.muscle_length
