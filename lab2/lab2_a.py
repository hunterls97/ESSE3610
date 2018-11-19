import numpy as np

def toRad(theta):
	return theta * (np.pi / 180)

def solve():
	#based on WGS1984 reference ellipsoid
	a = 6378206.4 #meters
	b = 6356583.8 #meters

	phi_A = toRad(43.7) #point A latitude
	phi_B = toRad(46.4) #point B latitude
	phi_M = (phi_A + phi_B) / 2 #mean of latitudes

	lam_A = toRad(280.367) #point A longitude
	lam_B = toRad(350.533) #point B longitude
	lam_M = (lam_A + lam_B) / 2 #mean of longitudes

	dl = lam_B - lam_A #delta longitude
	dp = phi_B - phi_A #delta latitude

	e = np.sqrt((a**2 - b**2)/a**2) #eccentricity

	Na = a / np.sqrt(1 - ((e**2)*(np.sin(phi_A)**2)))
	Nb = a / np.sqrt(1 - ((e**2)*(np.sin(phi_B)**2)))
	Nm = (Na + Nb) / 2

	Ma = a * (1 - e**2) / ((1 - ((e**2)*(np.sin(phi_A)**2)))**(3/2))
	Mb = a * (1 - e**2) / ((1 - ((e**2)*(np.sin(phi_B)**2)))**(3/2))
	Mm = (Ma + Mb) / 2

	#A function to get the next iteration
	def getNextIter(aijk, sijk):
		T1 = (dl*Nb / np.arccos(phi_B))
		T1 += (((sijk**3)/((Nb**2)))*(np.sin(aijk)))
		T1 -= ((sijk/(6 * (Nb**2)))*(np.sin(aijk)**3)*(np.arccos(phi_B)**2))

		T2 = dp*(Ma / (1 - ((3*(e**2)*np.sin(phi_A)*np.cos(phi_A)*dp) / (2*(1 - ((e**2)*(np.sin(phi_A)**2))))))) 
		T2 += (((sijk**2)*np.tan(phi_A)*(np.sin(aijk)**2)) / (2*Na)) 
		T2 += (((sijk**3)*np.cos(aijk)*(np.sin(aijk)**2)*(1 + (3*(np.tan(phi_A)**2)))) / (6*(Na**2)))

		aijk1 = np.arctan(T1/T2)
		sijk1 = T1 / np.sin(aijk1)

		return (aijk1, sijk1)

	#determine initial values for a and s
	aij = np.arctan((dl*Nb / np.arccos(phi_B)) / ((dp*Ma) / (1 - ((3*(e**2)*np.sin(phi_A)*np.cos(phi_A)*dp) / (2*(1 - ((e**2)*(np.sin(phi_A)**2))))))))
	sij = (dl * Nb) / (np.arccos(phi_B) * np.sin(aij))

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

	#determine the azimuth in the other direction
	da = (dl*np.sin(phi_M)*np.arccos(dp/2)) + (((dl**3)/12) * ((np.sin(phi_M)*np.arccos(dp/2)) - ((np.sin(phi_M)**3)*(np.arccos(dp/2)**3))))
	aji = aij + da + np.pi

	print("aji")
	print(aji)

	#highest point
	am = (aij + aji) / 2 #mean of azimuths

	#the result will be the difference in angle 
	dp_h = (sij * np.cos(am)) / Mm
	dl_h = (sij * np.arccos(phi_M) * np.sin(am)) / Nm

	print("The highest point occurs at: \n")
	print("latitude: " + str(dp_h) + "\n")
	print("longitude: " + str(dl_h) + "\n")

if __name__ == "__main__":
	solve()
