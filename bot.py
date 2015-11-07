import mapExtractor
import matplotlib.pyplot as plt
import datetime
import tetragonDetector
import random
import os
from time import sleep

from skimage import io 
import autopy
import captchaExtractor
import english
import alphaBotUtility
import report

x_ok = None
y_ok = None

def clickCoordinate(x, y):
	"""
	Clicks coordinate x, y
	"""
	autopy.mouse.smooth_move(x, y)
	autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

def clickOK():
	"""
	Clicks the OK of the 'click the rectangle' notification
	"""
	global x_ok
	global y_ok

	if None == x_ok:
		x_ok = mapExtractor.getOKPosition()[0]
	if None == y_ok:
		y_ok = mapExtractor.getOKPosition()[1]

	clickCoordinate(x_ok, y_ok)

def run(handleOK=False, debug=False):
	"""
	Runs the bot
	"""

	print english.produce_fuel
	coordinate = mapExtractor.getFuelstation()

	if None == coordinate:
		raise ValueError("Map positions are not initialized")

	print english.move_mouse_to_browser
	print english.start_in 
	alphaBotUtility.countDownwards(5)

	infix = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")

	currentRun = 0

	while True:

		currentReport = report.Report()

		if handleOK:
			clickOK()

		backgroundLayerPath = captchaExtractor.extractBackgroundLayer(coordinate[0], coordinate[1], nameInfix=infix)
		currentReport.setBackgroundLayer(backgroundLayerPath)

		# move to factory
		autopy.mouse.smooth_move(coordinate[0], coordinate[1])

		# extract capture
		captchaPath = captchaExtractor.extractCaptcha(coordinate[0], coordinate[1], nameInfix=infix)
		currentReport.setCaptcha(captchaPath)
		
		delta_x = None
		delta_y = None 

		(delta_x, delta_y) = tetragonDetector.findTetragonLineBased(captchaPath, report=currentReport, backgroundLayerPath=backgroundLayerPath, _debug=False)

		if not None == delta_x and not None == delta_y:
			target_x = int(coordinate[0] - 50 + delta_x)
			target_y = int(coordinate[1] + delta_y)

		currentReport.setTargetCoordinates(delta_x, delta_y)

		# move the mouse to prevent the blackening of the screen
		autopy.mouse.smooth_move(coordinate[0]-random.randint(0,100), coordinate[1]-random.randint(0,100))

# move to detected tetragon and click
		if not None == delta_x and not None == delta_y:
			clickCoordinate(target_x, target_y)

		currentReport.save("report_" + str(currentRun) + ".txt")
		currentRun += 1

# wait 60 seconds
		alphaBotUtility.countDownwards(60)
