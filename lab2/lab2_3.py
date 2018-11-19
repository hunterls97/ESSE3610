import numpy as np

def toRad(theta):
	return theta * (np.pi / 180)

def solve():
	#based on clarke 1866 reference ellipsoid
	a = 6378206.4 #meters
	b = 6356583.8 #meters

	#calculate flatening and eccentricity
	f = (a - b) / a
	e = np.sqrt((a**2 - b**2)/a**2)

	x0 = -25.82
	y0 = 168.10
	z0 = 167.31

	phi = toRad(44.295)
	lam = toRad(90.89)
	h = 260.26

	N = a / np.sqrt(1 - ((e**2)*(np.sin(phi)**2)))

	#Calculate cartesian components and apply transformations
	X = (N + h)*np.cos(phi)*np.cos(lam) + x0
	Y = (N + h)*np.cos(phi)*np.sin(lam) + y0
	Z = (N*((b**2)/(a**2)) + h)*np.sin(phi) + z0

	#PART B
	#using WGS1984 reference ellipsoid, redifine parameters
	a = 6378137 #meters
	b = 6356752.3142 #meters

	f = (a - b) / a
	e = np.sqrt((a**2 - b**2)/a**2)

	#Satellite geocentric coordinates
	xs = 4948685.566
	ys = -3249478.132
	zs = 3418646.589

	#Find distance of satellite with respect to geocenter
	P = np.sqrt((xs**2) + (ys**2) + (zs**2))
	print(P)

	#setup iteration variables
	h = 0
	phi_0 = np.arctan((zs/P) * (1 / (1 - e**2)))
	N_0 = (a**2) / np.sqrt((a**2)*(np.cos(phi_0)**2) + (b**2)*(np.sin(phi_0)**2))
	h_0 = (P / np.cos(phi_0)) - N_0

	#get the next iteration
	def getNextIter(p, n, h):
		_p = np.arctan(zs / P) / (1 - ((e**2)*n) / (n + h))
		_n = (a**2) / np.sqrt((a**2)*(np.cos(p)**2) + (b**2)*(np.sin(p)**2))
		_h = (P / np.cos(p)) - n

		return (_p, _n, _h)

	(phi_1, N_1, h_1) = getNextIter(phi_0, N_0, h_0)
	dp = np.abs(phi_1 - phi_0)
	dN = np.abs(N_1 - N_0)
	dh = np.abs(h_1 - h_0)

	#loop while there is a large enough difference between iterations
	while dp > 10**(-9) or dN > 10**(-9) or dh > 10**(-9):
		#set the last iteration values
		phi_0 = phi_1
		N_0 = N_1
		h_0 = h_1

		#get the next iteration values
		(phi_1, N_1, h_1) = getNextIter(phi_0, N_0, h_0)

		#find the difference to determine whether or not to keep iterating
		dp = np.abs(phi_1 - phi_0)
		dN = np.abs(N_1 - N_0)
		dh = np.abs(h_1 - h_0)

		#display the iteration results
		print(phi_1)
		print(N_1)
		print(h_1)
		print("\n")

	#convert back to degrees
	phi = (phi_1 * (180 / np.pi)) % 90
	h = h_1 

	#determine the latitude and convert to degrees
	lam = (2*np.arctan(ys / (xs + P)) * (180 / np.pi)) % 360

	print("the geodetic curvilinear coordinates are:")
	print("latitdue: " + str(phi) + " degrees north")
	print("longitude: " + str(lam) + " degrees east")
	print("height: " + str(h) + " meters")

if __name__ == "__main__":
	solve()
