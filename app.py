import sys
import numpy as np 

from ui import ui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CoordinateTransformer(QWidget):
	def __init__(self):
		super().__init__()

		#set the ui window parameters
		self.setGeometry(100, 100, 800, 800)

		#load basic styles
		with open('./ui/styles.css', 'r') as styles:
			self.setStyleSheet(styles.read())

		'''
		defines a graph of coordinate systems where the verticies are the specific coordinate systems
		the edges are the transformations to other coordinate systems, the first index in the tuple
		is the descriptive function that explains how to perform the transformation
		'''
		self.systems = {
			'Local Astronomical': (self.LASetup, ['Instantaneous Terrestrial']),
			'Instantaneous Terrestrial': (self.ITSetup, ['Local Astronomical', 'Apparent Place', 'Conventional Terrestrial']),
			'Apparent Place': (self.APSetup, ['Instantaneous Terrestrial', 'True Right Ascension']),
			'Conventional Terrestrial': (self.CTSetup, ['Instantaneous Terrestrial']),
			'True Right Ascension': (self.TRASetup, ['Apparent Place', 'Mean Right Ascension (T)']),
			'Mean Right Ascension (T)': (self.MRASetup, ['True Right Ascension', 'Ecliptic']),
			#'Mean Right Ascension (T0)': (self.MRA0Setup, ['Mean Right Ascension (T)', 'Ecliptic']),
			'Ecliptic': (self.ESetup, ['Mean Right Ascension (T)'])
		}

		#initialize variables
		self.longitude = 0
		self.latitude = 0
		self.x = 0
		self.y = 0
		self.z = 0
		self.x0 = 0
		self.y0 = 0
		self.z0 = 0
		self.julianDay0 = 0
		self.year = 0
		self.month = 0
		self.day = 0
		self.hour = 0
		self.minutes = 0
		self.seconds = 0

		#define the transform graph based on the dictionary of systems
		self.transformer = self.TransformGraph(self.systems)

		#initialize the ui component
		ui.initUI(self)

	#basic graph data structure to allow easy path finding for coordinate transformations
	class TransformGraph(object):

		#set the graph to the descriptive dictionary
		def __init__(self, description: dict):
			self.graph = description

		#get the verticies (unused)
		def verticies(self):
			return list(self.graph.keys())

		#add a vertex
		def addVertex(self, vertex):
			if not vertex in self.graph:
				self.graph[vertex] = []

		#get the edges (unused)
		def edges(self):
			return self.generateEdges()

		#add an edge (each edge is a coordinate transformation)
		def addEdge(self, edge):
			edge = set(edge)
			(v1, v2) = tuple(edge)

			if v1 in self.graph:
				self.graph[v1][1].append(v2)
			else:
				self.graph[v1][1] = [v2]

		#gets the edges (unused)
		def generateEdges(self):
			edges = []

			for v in self.graph:
				for n in self.graph[v][1]:
					if {n, v} not in edges:
						edges.append({v, n})

			return edges

		#finds the optimal (in our case only) path between coordinate systems
		def getPath(self, start, end, path=None):
			if path == None:
				path = []

			graph = self.graph
			path = path + [start]

			if start == end:
				return path
			
			if start not in graph:
				return None

			for v in graph[start][1]:
				if v not in path:
					ext = self.getPath(v, end, path)

					if ext:
						return ext

			return None

	#julian day calculator (given by TA) modified to allow hour/minute/second precision
	#using a formula that is gives values closer to online ones (I found that most online calculators
	#read a value given by this formula instead of the on given by the TA) 
	def JD(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0):
		#A = int(year/100)
		#B = int(A/4)
		#C = 2 - A + B
		#E = 365.25 * (year + 4716)
		#F = 30.6001 * (month + 1)
		#JD = C + day + E + F - 1524.5

		A = int((14 - month)/12)
		Y = year + 4800 - A
		M = month + (12*A) - 3

		JD = day + int((153*M+2)/5) + Y*365 + int(Y/4) - int(Y/100) + int(Y/400) - 32045.5
		JD = JD + (hour / 24) + (minute / (24 * 60)) + (second / (24 * 60 * 60))

		return JD

	#simple function to generate parameters that are used commonly by the coordinate
	#transformation functions (formulae found from slides, text, and web)
	def generateParameters(self):
		D = self.julianDay0 - 2451545 #Julian day (without hour/min/sec)
		H = self.hour #current hour
		T = D / 36525 

		#greenwhich mean sidereal time
		GMST = 6.697374558 + (0.06570982441908*D) + (1.00273790935*H) + (0.000026*(T**2))

		O = 125.04 - (0.052954 * D) * (np.pi / 180) #mean longitude of ascending node of moon
		L = 280.47 + (0.98565 * D) * (np.pi / 180)  #mean longitude of sun
		E = 23.4393 - (0.0000004 * D) * (np.pi / 180) #obliquity

		self.de = 0.0026*np.cos((125 - (0.0529 * D)) * (np.pi / 180)) + 0.0002*np.cos((200.9 + 1.97129*D) * (np.pi/180)) #nutation in obliquity
		self.dw = (-0.000319*np.sin(O) - 0.000024*np.sin(2*L)) * (np.pi / 180) #nutation in longitude (in radians)

		eqeq = (1/15) * (self.dw * np.cos(E) + (0.00264/60)*np.sin(O) + (0.000063/60)*np.sin(2*O)) #equation of equinoxes (from text)

		self.GAST = GMST + eqeq #greenwhich apparent sidereal time

		#aberration
		#max is 20 arcseconds
		maxA = 20/3600 * (np.pi / 180) #radians
		self.aberrationCorrection = maxA * (np.cos(((np.pi / 6) * self.month) + (np.pi / 3)) + np.sin(((np.pi / 6) * self.month) + (np.pi / 3))) #abberation correction depending on month

		#parallax
		maxP = 0.8/3600 * (np.pi / 180) #radians
		self.parallaxCorrection = maxP * (np.cos(((np.pi / 6) * self.month) + (np.pi / 3)) + np.sin(((np.pi / 6) * self.month) + (np.pi / 3))) #parallax correction depending on month

		#polar motion
		self.xp = 0.001535
		self.yp = xp


	#define a function to get a rotation matrix about the x-axis
	def Rx(self, theta):
		# define the cos and sine variables
		c,s = np.cos(theta), np.sin(theta)

		#return the rotation matrix
		return np.matrix([[1, 0, 0],
											[0, c, s],
											[0,-s, c]])

	#define a function to get a rotation matrix about the y-axis
	def Ry(self, theta):
		#define the cos and sine variables
		c,s = np.cos(theta), np.sin(theta)

		#return the rotation matrix
		return np.matrix([[c, 0,-s],
											[0, 1, 0],
											[s, 0, c]])

	#define a function to get a rotation matrix about the z-axis
	def Rz(self, theta):
		#define the cos and sine variables
		c,s = np.cos(theta), np.sin(theta)

		#return the rotation matrix
		return np.matrix([[c, s, 0],
											[-s, c, 0],
											[0, 0, 1]])

	#define a function to get the reflection about the y-axis
	def Py(self):
		return np.matrix([[1, 0, 0],
											[0, -1, 0],
											[0, 0, 1]])

	#define a function to get the current transformation coordinates as a column matrix (vector)
	def xyz(self):
		return np.matrix([[self.x],
										 [self.y],
										 [self.z]])

	#The following setup functions describe the order in which to do operations
	#to get to a certain coordinate system from another coordinate system.
	#example: to get to the local astronomical coordinate system from the instantaneous
	#terrestrial coordinate system, we take R2^-1(pi/2 - lattitude) * R3^-1((pi - longitude)) * {XYZ}
	#Notice that by multiplying the rotations by their respective inverses, we obtain the transformations
	#required to get the Instantaneous Terrestrial from the Local Astronomical
	def LASetup(self):
		return {
			'Instantaneous Terrestrial': [np.linalg.inv(self.Py()), np.linalg.inv(self.ry(np.pi / 2) - self.latitude), np.linalg.inv(self.Rz(np.pi - self.longitude)), self.xyz()]
		}

	def ITSetup(self):
		return {
			'Local Astronomical': [self.Rz(np.pi - self.longitude), self.Ry((np.pi / 2) - self.latitude), self.Py(), self.xyz()],
			'Apparent Place': [np.linalg.inv(self.Rz(-self.GAST)), self.xyz()],
			'Conventional Terrestrial': [self.Rx(self.yp), self.Ry(self.xp), self.xyz()]
		}

	#gast equation based on http://aa.usno.navy.mil/faq/docs/GAST.php
	def APSetup(self):
		return {
			'Instantaneous Terrestrial': [self.Rz(-self.GAST), self.xyz()],
			'True Right Ascension': [self.Rx(self.aberrationCorrection + self.parallaxCorrection), self.xyz()]
		}

	def CTSetup(self):
		return {
			'Instantaneous Terrestrial': [np.linalg.inv(self.Ry(self.xp)), np.linalg.inv(self.Rx(self.yp)), self.xyz()]
		}

	def TRASetup(self):
		return {
			'Apparent Place': [np.linalg.inv(self.Rx(self.aberrationCorrection + self.parallaxCorrection)), self.xyz()],

			#where 23.4*np.pi/180 is the inclination of the ecliptic in radians, de is the nutation of the obliquity, and dw is the nutation of the longitude
			'Mean Right Ascension (T)': [self.Rx(-(23.4 * np.pi/180) - self.de), self.Rz(self.dw), self.Rx((23.4 * np.pi/180)), self.xyz()]
		}

	def MRASetup(self):
		return {
			'True Right Ascension': [np.linalg.inv(self.Rx((23.4 * np.pi/180))), np.linalg.inv(self.Rz(self.dw)), np.linalg.inv(self.Rx(-(23.4 * np.pi/180) - self.de)), self.xyz()],
			#'Mean Right Ascension(T0)': [],
			'Ecliptic': [self.Rx(23.4 * np.pi/180), self.xyz()]
		}

	'''def MRA0Setup(self):
		return {
			'Mean Right Ascension(T)': [],
			'Ecliptic': []
		}'''

	def ESetup(self):
		return {
			'Mean Right Ascension (T)': [np.linalg.inv(self.Rx(23.4 * np.pi/180)), self.xyz()]
		}

if __name__ == "__main__":
	print('ESSE3610 Lab Group 6 - Part C')

	app = QApplication(sys.argv)
	Coords = CoordinateTransformer()
	Coords.show()
	sys.exit(app.exec_())
