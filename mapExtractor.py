from skimage import io 
import matplotlib.pyplot as plt
import numpy
import skimage
import autopy 

from skimage.feature import match_template

# position of each factory - stored as dict
factoryPosition = None

# position of the OK-button for retrieving after clicking
# on a false positive
OK_pos = None

def findTemplateInImage(templatePath, imagePath, debug=False):
	"""
	Returns the position of a template in an image
	"""
# load template
	template = skimage.transform.rescale(io.imread(templatePath), 0.5)
	if debug:
		plt.imshow(template)
		plt.title("Template")
		plt.show()

# load image 
	image = io.imread(imagePath, False);
	image = skimage.transform.rescale(image, 0.5)
	if debug:
		plt.imshow(image)
		plt.title("Image")
		plt.show()

# find building position
	result = match_template(image, template)
	result = result.squeeze()
	ij = numpy.unravel_index(numpy.argmax(result), result.shape)
	x, y = ij[::-1]

# add image midpoint
	x += int(float(len(template[:]))/2)
	y += int(float(len(template))/2)

# re-rescale ;)
	return numpy.array([x*2, y*2])

def initializeOK(debug=False):
	"""
	Determines the position of the OK button
	"""
	global OK_pos

# take screenshot
	screenshotPath = "tempOK.png"
	b = autopy.bitmap.capture_screen()
	b.save(screenshotPath)

	OK_pos = findTemplateInImage("./templates/OK.png", screenshotPath) 

def initialize(debug=False, progressFunc=None):
	"""
	Extracts the factory positions from a grabbed screenshot
	The 'progressFunc' is called with the made progress in procent.
	"""
	global factoryPosition

	factoryPosition = {}

# take screenshot
	screenshotPath = "temp.png"
	b = autopy.bitmap.capture_screen()
	b.save(screenshotPath)

	factoryPosition["fuelstation"] = findTemplateInImage("./templates/fuelstation.png", screenshotPath) 
	if not None == progressFunc:
		progressFunc(100)
#	factoryPosition["steelworks"] = findTemplateInImage("./templates/steelwork.png", screenshotPath) 
#	if not None == progressFunc:
#		progressFunc(50)
#	factoryPosition["carbonworks"] = findTemplateInImage("./templates/carbonwork.png", screenshotPath) 
#	if not None == progressFunc:
#		progressFunc(75)
#	factoryPosition["cementworks"] = findTemplateInImage("./templates/cementwork.png", screenshotPath) 
#	if not None == progressFunc:
#		progressFunc(100)

def getBuildingPosition(building_name):
	global factoryPosition
	
	if None == factoryPosition:
		return None
	
	return factoryPosition[building_name]

def getSteelworks():
	return getBuildingPosition("steelworks") 

def getFuelstation():
	return getBuildingPosition("fuelstation")

def getCarbonworks():
	return getBuildingPosition("carbonworks")

def getCementworks():
	return getBuildingPosition("cementworks")

def getOKPosition():
	global OK_pos

	return OK_pos
