import numpy as np

def toRad(theta):
	return theta * (np.pi / 180)

def solve():
	#based on WGS1984 reference ellipsoid
	a = 6378137 #meters
	b = 6356752.3142 #meters

	phi_A = toRad(43.7) #point A latitude
	phi_B = toRad(46.4) #point B latitude

	lam_A = toRad(280.367) #point A longitude
	lam_B = toRad(350.533) #point B longitude

	dl = lam_B - lam_A #delta longitude
	dp = phi_B - phi_A #delta latitude

	e = np.sqrt((a**2 - b**2)/a**2) #eccentricity

	Na = a / np.sqrt(1 - ((e**2)*(np.sin(phi_A)**2)))
	Nb = a / np.sqrt(1 - ((e**2)*(np.sin(phi_B)**2)))

	Ma = a * (1 - e**2) / ((1 - ((e**2)*(np.sin(phi_A)**2)))**(3/2))
	Mb = a * (1 - e**2) / ((1 - ((e**2)*(np.sin(phi_B)**2)))**(3/2))

	#A function to get the next iteration
	def getNextIter(aijk, sijk):
		T1 = (dl*Nb / np.arccos(phi_B)) + (((sijk**3)/(6*(Nb**2)))*np.sin(aijk)) - ((sijk/(6 * (Nb**2)))*(np.sin(aijk)**3)*(np.arccos(phi_B)**2))

		T2 = dp*(Ma / (1 - ((3*(e**2)*np.sin(phi_A)*np.cos(phi_A)*dp) / (2*(1 - ((e**2)*(np.sin(phi_A)**2)))))))
		+ (((sijk**2)*np.tan(phi_A)*(np.sin(aijk)**2)) / (2*Na))
		+ (((sijk**3)*np.cos(aijk)*(np.sin(aijk)**2)*(1 + 3*(np.tan(phi_A)**2))) / (6*(Na**2)))

		aijk1 = np.arctan(T1/T2)

		#the given derivation was wrong, it should be t2 /sin or t1/cos
		sijk1 = T2 / np.sin(aijk1)

		return (aijk1, sijk1)

	#determine initial values for a and s
	aij = np.arctan((dl*Nb / np.arccos(phi_B)) / ((dp*Ma) / (1 - ((3*(e**2)*np.sin(phi_A)*np.cos(phi_A)*dp) / (2*(1 - ((e**2)*(np.sin(phi_A)**2))))))))
	sij = (dl * Nb) / (np.arccos(phi_B) * np.sin(aij))
	#sij2 = (dp / np.cos(aij)) * (Ma / (1 - ((3*(e**2)*np.sin(phi_A)*np.cos(phi_A)*dp) / (2*(1 - ((e**2)*(np.sin(phi_A)**2)))))))

	#save the values to determine the change
	aijkm = aij
	sijkm = sij

	#get the new values
	aij, sij = getNextIter(aij, sij)

	#display the initial values
	print(aij)
	print(sij)

	#display the change in values from the previous iteration 
	print(np.abs(aijkm - aij))
	print(np.abs(sijkm - sij))

	#while the change in iterations isnt below a certain threshold
	while np.abs(aijkm - aij) > 10**(-9):
		aijkm = aij
		sijkm = sij

		#get next iteration
		aij, sij = getNextIter(aij, sij)

		#display the values of the current iterations
		print("AIJ")
		print(aij)
		print(np.abs(aijkm - aij))

		print("SIJ")
		print(sij)
		print(np.abs(sijkm - sij))

if __name__ == "__main__":
	solve()
