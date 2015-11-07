from skimage import io
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lineFinding')))
import numpy
import imageProcessing
import matplotlib.pyplot as plt
import lineFinding
import postProcessing
from scipy.spatial import ConvexHull

debug = False

_image = None

debug_show_combined_lines = True 
debug_show_image_processing = False 
debug_show_result = True 

keywords = [
#			"scatter", 
#			"linecount", 
#			"tetragonshape", 
#			"structure_mean_length",
#			"rate_structures",
#			"target"
			]

def printd(text, keyword=None):
	global debug
	global keywords

	if not debug:
		return

	if not None == keyword and not keyword in keywords:
		return

	print str(text)

def plotStructures(image, structures):
	plt.imshow(image, cmap=plt.cm.gray)
	colors = ['red', 'green', 'blue', 'cyan', 'magenta']
	i = 0
	for line in structures:
		line = lineFinding.transformLineSegmentsIntoNumpyArray(line)
		for li in line:
			plt.plot([li[0], li[2]], [li[1], li[3]] , linewidth=2, color=colors[i % len(colors)])
		i += 1

	plt.show()

def tetragonShape(structure, epsilon=20):
	rightCorners = 0

	for i in range(len(structure)):
		for j in range(i + 1, len(structure)):
			if not postProcessing.isAdjacent(structure[i], structure[j], delta=2):
				continue
			angle = postProcessing.computeAngle(structure[i], structure[j])
			printd("\tAngle between " + str(structure[i]) + " - " + str(structure[j]) + ": " + str(angle), "tetragonshape")

			if 90 - epsilon <= angle and angle <= epsilon + 90:
				rightCorners += 1
				printd("\t --> right corner (#" + str(rightCorners) + ")", "tetragonshape")

	return rightCorners >= 2

def rateStructure(structures):
	"""
	Take the structure that contains the least points within its complex hull
	"""
	bestStructure = None
	bestValue = -1
	i = 0
	for structure in structures:
		printd("Rate structure: " + str(structure), "rate_structures")
		points = []

		for line in structure:
			points.append(numpy.array([int(line.x_start), int(line.y_start)]))
			points.append(numpy.array([int(line.x_end), int(line.y_end)]))

		hull = ConvexHull(numpy.array(points))

		number_of_hull_points = len(hull.vertices)
		number_of_points = len(points)

		value = float(number_of_hull_points) / number_of_points

		printd("HP: " + str(number_of_hull_points) + "/" + str(number_of_points) + "-> Rating-value: " + str(value), "rate_structures")

		if value > bestValue:
			bestValue = value
			bestStructure = i
			printd("Update max value: " + str(bestValue) + " with index " + str(bestStructure), "rate_structures")

		i += 1


	return [structures[bestStructure]]


def getClickPointOfStructure(structure):
	points = []
	for line in structure:
		points.append(numpy.array([int(line.x_start), int(line.y_start)]))
		points.append(numpy.array([int(line.x_end), int(line.y_end)]))

	hull = ConvexHull(numpy.array(points))

	cx = numpy.mean(hull.points[hull.vertices,0])
	cy = numpy.mean(hull.points[hull.vertices,1])

	return (cx, cy)

def lineLengthMeanOfStructure(structure):

	length = 0
	count = 0
	for line in structure:
		length += line.getLineLength()
		count += 1

	return float(length) / count

def removeSmallScatter(structure, length):
	new_structure = []
	for line in structure:
		if not line.getLineLength() <= length:
			new_structure.append(line)

	return new_structure

def findTetragonLineBased(captchaPath, backgroundLayerPath=None, report=None, _debug=False):
	global debug
	global _image
	debug = _debug
	target_x = None
	target_y = None

# compute feature points
	points  = imageProcessing.processImage(captchaPath, report=report, backgroundLayerPath=backgroundLayerPath, debug=(debug and debug_show_image_processing), corner_min_dist=5)

	processedImageName = captchaPath[0:len(captchaPath)-4] + "_processed.png"
	image = io.imread(processedImageName, True)
	_image = image

	mean = image.mean()

	def isLineColor(color):
		return color > mean

	lines = lineFinding._findLines(image, isLineColor=isLineColor)

	structures = postProcessing.groupAdjacentLines(lines, delta=2)

	structures = postProcessing.combineLinesWithEqualSlope(structures, angle_epsilon=50)

	if debug and debug_show_combined_lines:
		plotStructures(image, structures)

	filteredStructures = []
	for structure in structures:

		printd("Structure before scatter: " + str(structure), "scatter")
		# remove scattering from every individual component
		structure = removeSmallScatter(structure, 5)
		printd("Structure after scatter: " + str(structure), "scatter")
		# single and double lines can not form a tetragon.
		# Also 3 lines can not form a tetragon but sometimes they
		# from an U and the fourth line is not attached
		if len(structure) <= 2 or len(structure) > 6:
			printd("Structure: " + str(structure), "linecount")
			printd( "--> Too much or too few lines", "linecount")
			continue
		else:
			if lineLengthMeanOfStructure(structure) >= 7:
				if tetragonShape(structure):
					(target_x, target_y) = getClickPointOfStructure(structure)
					filteredStructures.append(structure)
				else:
					printd("Structure: " + str(structure), "tetragonshape")
					printd("--> no tetragon shape", "tetragonshape")
			else:
				printd("Structure: " + str(structure), "structure_mean_length")
				printd("--> too short", "structure_mean_length")

	structures = filteredStructures

	if len(structures) > 1:
		printd("Rating structures", "rate_structures")
		structures = rateStructure(structures)
		(target_x, target_y) = getClickPointOfStructure(structures[0])

	if debug and debug_show_result:
		plotStructures(image, structures)

	printd("Target-x: " + str(target_x) + ", Target-y: " + str(target_y), "target")

	return (target_x, target_y)

def test():

# list of captchas that must always work -- provide a good coverage
	print str(findTetragonLineBased("./captcha/capt.png", "./captcha/capt_bg.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_02-11-15_22-56-40.png", "./captcha/captcha_bg_02-11-15_22-56-40.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_12-44-35.png", "./captcha/captcha_bg_03-11-15_12-44-35.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_12-48-34.png", "./captcha/captcha_bg_03-11-15_12-48-34.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_15-19-50.png", "./captcha/captcha_bg_03-11-15_15-19-50.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_15-28-59.png", "./captcha/captcha_bg_03-11-15_15-28-59.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_20-08-38.png", "./captcha/captcha_bg_03-11-15_20-08-38.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_03-11-15_22-29-41.png", "./captcha/captcha_bg_03-11-15_22-29-41.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_05-11-15_19-44-52.png", backgroundLayerPath="./captcha/captcha_bg_05-11-15_19-44-52.png", report=None,  _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_06-11-15_00-33-45.png", backgroundLayerPath="./captcha/captcha_bg_06-11-15_00-33-45.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_06-11-15_01-16-09.png", backgroundLayerPath="./captcha/captcha_bg_06-11-15_01-16-09.png", report=None, _debug=True))
	print str(findTetragonLineBased("./captcha/captcha_06-11-15_13-06-15.png", backgroundLayerPath="./captcha/captcha_bg_06-11-15_13-06-15.png", report=None, _debug=True))
if __name__ == '__main__':
	test()
