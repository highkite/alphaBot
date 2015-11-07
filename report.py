import datetime
import os

reportDirectory = None

class Report(object):
	"""
	Is used the track the current run. Thus it is easier
	to identify situations that causes errors.
	"""
	_report = []

	def __init__(self):
		self._report = []
		self.setTime()

	def setTime(self):
		time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
		self._report.append("Time: " + str(time) + "\n")

	def setBackgroundLayer(self, path):
		"""
		Sets the path of the background layer in the report
		"""
		self._report.append("backgroundlayer: " + str(path) + "\n")

	def setCaptcha(self, path):
		"""
		Sets the path of the captcha in the report
		"""
		self._report.append("captchaPath: " + str(path) + "\n")

	def setProcessedImage(self, path):
		"""
		Sets the path of the processed image in the report
		"""
		self._report.append("processedImage: " + str(path) + "\n")

	def setTargetCoordinates(self, x_target, y_target):
		"""
		Sets the target coordinates in the report
		"""
		self._report.append("x_target: " + str(x_target) + "\n")
		self._report.append("y_target: " + str(y_target) + "\n")

	def append(self, text):
		"""
		Appends a string to the report
		"""
		self._report.append(text)

	def save(self, name):
		"""
		Saves the report into a file
		"""
		global reportDirectory

		if None == reportDirectory:
			infix = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")

			reportDirectory = "./reports/reports_" + str(infix)

			if not os.path.exists(reportDirectory):
				os.makedirs(reportDirectory)

		f = open(reportDirectory + "/" + name, 'w+')
		for text in self._report:
			f.write(text)
		f.close()

