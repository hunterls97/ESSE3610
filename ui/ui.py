import sys
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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

	def timeChange(year, month, day, hour, minutes, seconds):
		self.year = int(year if year else 0)
		self.month = int(month if month else 0)
		self.day = int(day if day else 0)
		self.hour = int(hour if hour else 0)
		self.minutes = int(minutes if minutes else 0)
		self.seconds = int(seconds if seconds else 0)

		self.julianDay0 = self.JD(self.year, 
														  self.month, 
														  self.day)

		self.julianDay = self.JD(self.year, 
														 self.month, 
														 self.day, 
														 self.hour, 
														 self.minutes, 
														 self.seconds)

	def xChange(x):
		self.x0 = x

	def yChange(y):
		self.y0 = y

	def zChange(z):
		self.z0 = z

	#this will be very confusing to read lol
	def calculate(f, t):
		paths = self.transformer.getPath(f, t)

		self.x = self.x0
		self.y = self.y0
		self.z = self.z0

		self.generateParameters()

		for i, p in enumerate(paths):
			if i > 0:
				prev = paths[i - 1]
				I = np.matrix([[1,0,0],
											[0,1,0],
											[0,0,1]])

				for op in self.systems[p][0]()[prev]:
					I = np.dot(I, op)

					print(I)
				
				self.x = I.item((0,0))
				self.y = I.item((1,0))
				self.z = I.item((2,0))

		self.xOut.setText(str(self.x))
		self.yOut.setText(str(self.y))
		self.zOut.setText(str(self.z))

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

	self.yearLabel = QLabel(self)
	self.yearLabel.setText('Year: ')
	self.yearLabel.move(10, 50)

	self.yearIn = QLineEdit(self)
	self.yearIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.yearIn.setProperty('type', 'time')
	self.yearIn.move(10, 80)

	self.monthLabel = QLabel(self)
	self.monthLabel.setText('Month (number): ')
	self.monthLabel.move(140, 50)

	self.monthIn = QLineEdit(self)
	self.monthIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.monthIn.setProperty('type', 'time')
	self.monthIn.move(140, 80)

	self.dayLabel = QLabel(self)
	self.dayLabel.setText('Day (number): ')
	self.dayLabel.move(270, 50)

	self.dayIn = QLineEdit(self)
	self.dayIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.dayIn.setProperty('type', 'time')
	self.dayIn.move(270, 80)

	self.hourLabel = QLabel(self)
	self.hourLabel.setText('Hour: ')
	self.hourLabel.move(400, 50)

	self.hourIn = QLineEdit(self)
	self.hourIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.hourIn.setProperty('type', 'time')
	self.hourIn.move(400, 80)

	self.minuteLabel = QLabel(self)
	self.minuteLabel.setText('Minute: ')
	self.minuteLabel.move(530, 50)

	self.minuteIn = QLineEdit(self)
	self.minuteIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.minuteIn.setProperty('type', 'time')
	self.minuteIn.move(530, 80)

	self.secondLabel = QLabel(self)
	self.secondLabel.setText('Second: ')
	self.secondLabel.move(660, 50)

	self.secondIn = QLineEdit(self)
	self.secondIn.setValidator(QDoubleValidator(-9999, 9999, 0))
	self.secondIn.setProperty('type', 'time')
	self.secondIn.move(660, 80)

	self.longLabel = QLabel(self)
	self.longLabel.setText('longitude (degrees): ')
	self.longLabel.move(180, 120)

	self.longitudeEditor = QLineEdit(self)
	self.longitudeEditor.setValidator(QDoubleValidator(0,360,2))
	self.longitudeEditor.move(180, 150)

	self.longDirection = QComboBox(self)
	self.longDirection.addItems(['West', 'East'])
	self.longDirection.move(330, 150)

	self.latLabel = QLabel(self)
	self.latLabel.setText('latitude (degrees): ')
	self.latLabel.move(10, 120)

	self.latitudeEditor = QLineEdit(self)
	self.latitudeEditor.setValidator(QDoubleValidator(-90, 90, 2))
	self.latitudeEditor.move(10, 150)

	self.calculate = QPushButton(self)
	self.calculate.setText('Calculate')
	self.calculate.move(650, 150)

	self.xInLabel = QLabel(self)
	self.xInLabel.setText('Enter X Coordinate: ')
	self.xInLabel.move(10, 190)

	self.xIn = QLineEdit(self)
	self.xIn.setValidator(QDoubleValidator(0,360,2))
	self.xIn.move(10, 220)

	self.yInLabel = QLabel(self)
	self.yInLabel.setText('Enter Y Coordinate: ')
	self.yInLabel.move(10, 260)

	self.yIn = QLineEdit(self)
	self.yIn.setValidator(QDoubleValidator(0,360,2))
	self.yIn.move(10, 290)

	self.zInLabel = QLabel(self)
	self.zInLabel.setText('Enter Z Coordinate: ')
	self.zInLabel.move(10, 340)

	self.zIn = QLineEdit(self)
	self.zIn.setValidator(QDoubleValidator(0,360,2))
	self.zIn.move(10, 360)

	self.xOutLabel = QLabel(self)
	self.xOutLabel.setText('Transformed X: ')
	self.xOutLabel.move(650, 190)

	self.xOut = QLineEdit(self)
	self.xOut.setValidator(QDoubleValidator(0,360,2))
	self.xOut.setReadOnly(True)
	self.xOut.move(650, 220)

	self.yOutLabel = QLabel(self)
	self.yOutLabel.setText('Transformed Y: ')
	self.yOutLabel.move(650, 260)

	self.yOut = QLineEdit(self)
	self.yOut.setValidator(QDoubleValidator(0,360,2))
	self.yOut.setReadOnly(True)
	self.yOut.move(650, 290)

	self.zOutLabel = QLabel(self)
	self.zOutLabel.setText('Transformed Z: ')
	self.zOutLabel.move(650, 340)

	self.zOut = QLineEdit(self)
	self.zOut.setValidator(QDoubleValidator(0,360,2))
	self.zOut.setReadOnly(True)
	self.zOut.move(650, 360)

	self.systemsBoxFrom.activated.connect(lambda: sbfChange(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))
	self.systemsBoxTo.activated.connect(lambda: sbfChange(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))
	self.longitudeEditor.textChanged.connect(lambda: lonChange(float(self.longitudeEditor.text() if self.longitudeEditor.text() else 0), self.longDirection.currentText()))
	self.latitudeEditor.textChanged.connect(lambda: latChange(float(self.latitudeEditor.text() if self.latitudeEditor.text() else 0)))
	self.longDirection.activated.connect(lambda: lonChange(float(self.longitudeEditor.text() if self.longitudeEditor.text() else 0), self.longDirection.currentText()))
	self.xIn.textChanged.connect(lambda: xChange(float(self.xIn.text())))
	self.yIn.textChanged.connect(lambda: yChange(float(self.yIn.text())))
	self.zIn.textChanged.connect(lambda: zChange(float(self.zIn.text())))
	self.calculate.clicked.connect(lambda: calculate(self.systemsBoxFrom.currentText(), self.systemsBoxTo.currentText()))
	self.yearIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))
	self.monthIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))
	self.dayIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))
	self.hourIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))
	self.minuteIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))
	self.secondIn.textChanged.connect(lambda: timeChange(self.yearIn.text(), self.monthIn.text(), self.dayIn.text(), self.hourIn.text(), self.minuteIn.text(), self.secondIn.text()))