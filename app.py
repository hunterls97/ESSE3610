import sys
import numpy as np 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CoordinateTransformer(QWidget):
	def __init__(self):
		super().__init__()

		self.setGeometry(100, 100, 800, 800)

		with open('./styles.css', 'r') as styles:
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
			'True Right Ascension': (self.TRASetup, ['Apparent Place', 'Mean Right Ascension']),
			'Mean Right Ascension (T)': (self.MRASetup, ['True Right Ascension', 'Mean Right Ascension (T0)']),
			'Mean Right Ascension (T0)': (self.MRA0Setup, ['Mean Right Ascension (T)', 'Ecliptic']),
			'Ecliptic': (self.ESetup, ['Mean Right Ascension (T0)'])
		}

		self.longitude = 0
		self.latitude = 0
		self.x = 0
		self.y = 0
		self.z = 0

		self.transformer = self.TransformGraph(self.systems)
		self.initUI()

	def initUI(self):

		#ui events
		def sbfChange(f, t):
			print(self.transformer.getPath(f, t))

		def sbtChange(f, t):
			print(self.transformer.getPath(f, t))

		def latChange(latitude):
			self.latitude = latitude * (np.pi / 180) 

		def lonChange(longitude, direction):
			if direction == 'West':
				self.longitude = ((360 - longitude) % 360) * (np.pi / 180) 
			else:
				self.longitude = (longitude % 360) * (np.pi / 180)

		def xChange(x):
			self.x = x

		def yChange(y):
			self.y = y

		def zChange(z):
			self.z = z

		#this will be very confusing to read lol
		def calculate(f, t):
			paths = self.transformer.getPath(f, t)

			for i, p in enumerate(paths):
				if i > 0:
					prev = paths[i - 1]
					I = np.matrix([[1,0,0],
												[0,1,0],
												[0,0,1]])

					for op in self.systems[p][0](self.x, self.y, self.z)[prev]:
						I = np.dot(I, op)

						print(I)
					

		self.sbfLabel = QLabel(self)
		self.sbfLabel.setText('Select From Transformation: ')
		self.sbfLabel.move(10, 10)

		self.systemsBoxFrom = QComboBox(self)
		self.systemsBoxFrom.setObjectName('sbf')
		self.systemsBoxFrom.addItems(list(self.systems.keys()))
		self.systemsBoxFrom.move(190, 10)
		
		self.sbtLabel = QLabel(self)
		self.sbtLabel.setText('Select To Transformation: ')
		self.sbtLabel.move(410, 10)

		self.systemsBoxTo = QComboBox(self)
		self.systemsBoxTo.setObjectName('sbt')
		self.systemsBoxTo.addItems(list(self.systems.keys()))
		self.systemsBoxTo.move(580, 10)

		self.longLabel = QLabel(self)
		self.longLabel.setText('longitude (degrees): ')
		self.longLabel.move(180, 50)

		self.longitudeEditor = QLineEdit(self)
		self.longitudeEditor.setValidator(QDoubleValidator(0,360,2))
		self.longitudeEditor.move(180, 80)

		self.longDirection = QComboBox(self)
		self.longDirection.addItems(['West', 'East'])
		self.longDirection.move(330, 80)

		self.latLabel = QLabel(self)
		self.latLabel.setText('latitude (degrees): ')
		self.latLabel.move(10, 50)

		self.latitudeEditor = QLineEdit(self)
		self.latitudeEditor.setValidator(QDoubleValidator(-90, 90, 2))
		self.latitudeEditor.move(10, 80)

		self.calculate = QPushButton(self)
		self.calculate.setText('Calculate')
		self.calculate.move(650, 80)

		self.xInLabel = QLabel(self)
		self.xInLabel.setText('Enter X Coordinate: ')
		self.xInLabel.move(10, 120)

		self.xIn = QLineEdit(self)
		self.xIn.setValidator(QDoubleValidator(0,360,2))
		self.xIn.move(10, 150)

		self.yInLabel = QLabel(self)
		self.yInLabel.setText('Enter Y Coordinate: ')
		self.yInLabel.move(10, 190)

		self.yIn = QLineEdit(self)
		self.yIn.setValidator(QDoubleValidator(0,360,2))
		self.yIn.move(10, 220)

		self.zInLabel = QLabel(self)
		self.zInLabel.setText('Enter Z Coordinate: ')
		self.zInLabel.move(10, 260)

		self.zIn = QLineEdit(self)
		self.zIn.setValidator(QDoubleValidator(0,360,2))
		self.zIn.move(10, 290)

		self.xOutLabel = QLabel(self)
		self.xOutLabel.setText('Transformed X: ')
		self.xOutLabel.move(650, 120)

		self.xOut = QLineEdit(self)
		self.xOut.setValidator(QDoubleValidator(0,360,2))
		self.xOut.setReadOnly(True)
		self.xOut.move(650, 150)

		self.yOutLabel = QLabel(self)
		self.yOutLabel.setText('Transformed Y: ')
		self.yOutLabel.move(650, 190)

		self.yOut = QLineEdit(self)
		self.yOut.setValidator(QDoubleValidator(0,360,2))
		self.yOut.setReadOnly(True)
		self.yOut.move(650, 220)

		self.zOutLabel = QLabel(self)
		self.zOutLabel.setText('Transformed Z: ')
		self.zOutLabel.move(650, 260)

		self.zOut = QLineEdit(self)
		self.zOut.setValidator(QDoubleValidator(0,360,2))
		self.zOut.setReadOnly(True)
		self.zOut.move(650, 290)

		self.systemsBoxFrom.activated.connect(lambda: sbfChange(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))
		self.systemsBoxTo.activated.connect(lambda: sbfChange(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))
		self.longitudeEditor.textChanged.connect(lambda: lonChange(float(self.longitudeEditor.text() if self.longitudeEditor.text() else 0), self.longDirection.currentText()))
		self.latitudeEditor.textChanged.connect(lambda: latChange(float(self.latitudeEditor.text() if self.latitudeEditor.text() else 0)))
		self.longDirection.activated.connect(lambda: lonChange(float(self.longitudeEditor.text() if self.longitudeEditor.text() else 0), self.longDirection.currentText()))
		self.xIn.textChanged.connect(lambda: xChange(float(self.xIn.text())))
		self.yIn.textChanged.connect(lambda: yChange(float(self.yIn.text())))
		self.zIn.textChanged.connect(lambda: zChange(float(self.zIn.text())))
		self.calculate.clicked.connect(lambda: calculate(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))

	class TransformGraph(object):

		def __init__(self, description: dict):
			self.graph = description

		def verticies(self):
			return list(self.graph.keys())

		def addVertex(self, vertex):
			if not vertex in self.graph:
				self.graph[vertex] = []

		def edges(self):
			return self.generateEdges()

		def addEdge(self, edge):
			edge = set(edge)
			(v1, v2) = tuple(edge)

			if v1 in self.graph:
				self.graph[v1][1].append(v2)
			else:
				self.graph[v1][1] = [v2]

		def generateEdges(self):
			edges = []

			for v in self.graph:
				for n in self.graph[v][1]:
					if {n, v} not in edges:
						edges.append({v, n})

			return edges

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


		def __str__(self):
			res = "vertices: "

			for k in self.graph:
				res += str(k) + " "
				res += "\nedges: "

			for edge in self.generateEdges():
				res += str(edge) + " "

			return res

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

	#define a function to get the current transformation coordinates as a column matrix (vector)
	def xyz(self):
		return np.matrix([[self.x],
										 [self.y],
										 [self.z]])

	def LASetup(self, x, y, z):
		v = np.arcsin(z)
		A = y/(x + np.sqrt((x**2) + (y**2)))

		return 'LASetup'

	def ITSetup(self, x, y, z):
		print(self.latitude)
		return {
			'Local Astronomical': [self.Rz(np.pi - self.longitude), self.Ry((np.pi / 2) - self.latitude), self.xyz()],
			'Apparent Place': [],
			'Conventional Terrestrial': []
		}

	def APSetup(self, x, y, z):
		return 'APSetup'

	def CTSetup(self, x, y, z):
		return 'CTSetup'

	def TRASetup(self, x, y, z):
		return 'TRASetup'

	def MRASetup(self, x, y, z):
		return 'MRASetup'

	def MRA0Setup(self, x, y, z):
		return 'MRA0Setup'

	def ESetup(self, x, y, z):
		return 'ESetup'

if __name__ == "__main__":
	print('ESSE3610 Lab Group 6 - Part A')

	app = QApplication(sys.argv)
	Coords = CoordinateTransformer()
	Coords.show()
	sys.exit(app.exec_())
