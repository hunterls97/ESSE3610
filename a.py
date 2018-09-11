import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
	print('ESSE3610 Lab Group 6 - Part A')

	fig = plt.figure()

	#set figure and axes parameters
	ax = fig.gca(projection='3d')
	ax.set_xlim([-0.02, 0.02])
	ax.set_ylim([-0.02, 0.02])
	ax.set_zlim([-0.02, 0.02])

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

	#define the origin point in 3D as a tuple
	origin = (0,0,0)

	#define the original cordinates as a set of vectors normal to the xy, yz and xz planes
	O_norm = np.array([[0.01,0,0],[0,0.01,0],[0,0,0.01]])

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
