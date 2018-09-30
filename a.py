import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import sys

#Group Lab Number
gln = 6

#define a function to get a rotation matrix about the x-axis
def Rx(theta):
	# define the cos and sine variables
	c,s = np.cos(theta), np.sin(theta)

	#return the rotation matrix
	return np.matrix([[1, 0, 0],
										[0, c, s],
										[0,-s, c]])

#define a function to get a rotation matrix about the y-axis
def Ry(theta):
	#define the cos and sine variables
	c,s = np.cos(theta), np.sin(theta)

	#return the rotation matrix
	return np.matrix([[c, 0,-s],
										[0, 1, 0],
										[s, 0, c]])

#define a function to get a rotation matrix about the z-axis
def Rz(theta):
	#define the cos and sine variables
	c,s = np.cos(theta), np.sin(theta)

	#return the rotation matrix
	return np.matrix([[c, s, 0],
										[-s, c, 0],
										[0, 0, 1]])

#define a function to get the reflection about the y-axis
def Py():
	return np.matrix([[1, 0, 0],
										[0, -1, 0],
										[0, 0, 1]])

def q1():
	fig = plt.figure()

	#set figure and axes parameters
	ax = fig.gca(projection='3d')
	ax.set_xlim([-2, 2])
	ax.set_ylim([-2, 2])
	ax.set_zlim([-2, 2])
	ax.set_xlabel('x-axis')
	ax.set_ylabel('y-axis')
	ax.set_zlabel('z-axis')

	#define the origin point in 3D as a tuple
	origin = (0,0,0)

	#define the original cordinates as a set of vectors normal to the xy, yz and xz planes
	O_norm = np.array([[1,0,0],[0,1,0],[0,0,1]])

	#define the components of the coordinate system
	X,Y,Z = zip(*O_norm)

	#render the coordintes
	coords = ax.quiver(*origin, X, Y, Z, label='rotation')

	#get iterations of pi/60
	iters = np.linspace(0, 2*np.pi, 120)

	# rotate the axes and update
	for theta in iters:
		#ax.clear() #comment this line out to view the path sweeped by this rotation
		#render the new coordinate system after applying a small rotation based on the given rotation about the x-axis
		coords = ax.quiver(*origin, np.dot(Rx(theta), X), np.dot(Rx(theta), Y),	np.dot(Rx(theta), Z), label='rotation')

		#render the applied rotation
		plt.draw()
		plt.pause(.001)

	for theta in iters:
		#ax.clear() #comment this line out to view the path sweeped by this rotation
		#render the new coordinate system after applying a small rotation based on the given rotation about the y-axis
		coords = ax.quiver(*origin, np.dot(Ry(theta), X), np.dot(Ry(theta), Y),	np.dot(Ry(theta), Z), label='rotation')

		#render the applied rotation
		plt.draw()
		plt.pause(.001)

	plt.show()

def q2(R = Rx):
	#get iterations of pi/60
	iters = np.linspace(0, 2*np.pi, 120)

	for theta in iters:
		#Print the output for R(q)
		print('base case')
		print(R(theta))

		#print the output for R(-q)
		print('negative theta case')
		print(R(theta * -1))

		#print the output for R(q)^T
		print('transpose case')
		print(R(theta).T)

		#print the output for R(q)^-1
		print('inverse case')
		print(np.linalg.inv(R(theta)))


def q3():
	fig = plt.figure()

	#set figure and axes parameters
	ax = fig.gca(projection='3d')
	ax.set_xlim([-2, 2])
	ax.set_ylim([-2, 2])
	ax.set_zlim([-2, 2])
	ax.set_xlabel('x-axis')
	ax.set_ylabel('y-axis')
	ax.set_zlabel('z-axis')

	#define the origin point in 3D as a tuple
	origin = (0,0,0)

	#define the original cordinates as a set of vectors normal to the xy, yz and xz planes
	O_norm = np.array([[1,0,0],[0,1,0],[0,0,1]])

	#define the components of the coordinate system
	X,Y,Z = zip(*O_norm)

	#render the Oxyz
	ax.quiver(*origin, X, Y, Z, label='rotation')

	#Calculate the components of Ox'y'z'
	X = np.dot(np.dot(Ry(np.pi / 2), np.dot(Rz(-1 * np.pi / 6), np.dot(Py(), Rx((np.pi * gln / 4))))), X)
	Y = np.dot(np.dot(Ry(np.pi / 2), np.dot(Rz(-1 * np.pi / 6), np.dot(Py(), Rx((np.pi * gln / 4))))), Y)
	Z = np.dot(np.dot(Ry(np.pi / 2), np.dot(Rz(-1 * np.pi / 6), np.dot(Py(), Rx((np.pi * gln / 4))))), Z)

	#Render the transformation
	ax.quiver(*origin, X, Y, Z, label='rotation', color='black')

	plt.show()

if __name__ == "__main__":
	print('ESSE3610 Lab Group 6 - Part A')
	
	#pass 1 as an argument to do the setup/ question 1
	if len(sys.argv) > 1:
		if int(sys.argv[1]) == 1:
			q1()

		if int(sys.argv[1]) == 2:
			q2()

		if int(sys.argv[1]) == 3:
			q3()

	else:
		q1()

	
