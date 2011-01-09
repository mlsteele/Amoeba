import numpy
import random
import cake
import time

master = cake.c_master()
na = master.make_node(1, numpy.array([0., 0.]), i_vel=numpy.array([0.01, 0.]))
nb = master.make_node(1, numpy.array([5., 0.]))

frame = -1
while True:
	frame += 1
	
	master.update()
	
	print "\n" + str(frame)
	print na.pos
	print nb.pos
	time.sleep(.1)
