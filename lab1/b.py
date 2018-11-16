import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import sys

#Group Lab Number
gln = 6

def q1():
	#Since every andle is measured east and 280.185 is east, we converted it to a west angle (negative east direction)
	L = (360 - 280.185) #degrees west

	#values for the gast
	GAST_1 = 8.691 #degrees
	GAST_2 = 9.677 #degrees

	#values for the right ascension
	RA_1 = 64.845 #degrees
	RA_2 = 79.002 #degrees

	#values for the hour angle (to be interpolated)
	H_1 = GAST_1 + RA_1 - L
	H_2 = GAST_2 + RA_2 - L  

	#quantity of iterations
	iters = 500

	#interpolation
	Hs = np.linspace(H_1, H_2, iters)

	#flag to determine existance of h=0
	index = -1

	#iterate over the interpolation and find where the hour angle switches from negative to positive
	for i in range(0, len(Hs)):
		if Hs[i] > 0:
			index = i - 1
			break

	#determine the gast and right ascension for the index of the interpolation where the hour angle switches signs
	GAST = (((GAST_2 - GAST_1) / iters) * ((index + index+1)/2)) + GAST_1
	RA = (((RA_2 - RA_1) / iters) * ((index + index+1)/2)) + RA_1

	#print the values
	print(GAST)
	print(RA)
	print(GAST + RA - L)
	print(GAST_1 + RA_1 - L)

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