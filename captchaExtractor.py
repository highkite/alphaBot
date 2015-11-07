import autopy 
from skimage import io 
import matplotlib.pyplot as plt
import datetime

def extractScreenPart(x, y, width, height, name, debug=False):
	"""
	Extracts a part of the screen specified by x, y, width and height and
	stores it as 'name'
	"""
	c = autopy.bitmap.capture_screen()
	c.save("./tempPart.png")

	part = io.imread("./tempPart.png", False);

	part = part[y:y+height,x:x+width,:]

	if debug:
		plt.imshow(part)
		plt.title("Taken image part")
		plt.show()

	io.imsave(name, part)

	return name

def extractBackgroundLayer(x, y, nameInfix=None, debug=False):
	"""
	We extract the background from a capture to reduce unwanted noise.
	This function takes the corresponding background part
	"""

	if nameInfix == None:
		bgLayerName = "./captcha/captcha_bg_" + str(datetime.datetime.now().isoformat()) + ".png"
	else:
		bgLayerName = "./captcha/captcha_bg_" + str(nameInfix) + ".png"

	return extractScreenPart(x-50, y+5, 170, 60, name=bgLayerName, debug=debug)

def extractCaptcha(x, y, nameInfix=None, debug=False):
	"""
	Extracts the captcha from the building on position (x,y)
	"""

	if nameInfix == None:
		captchaName = "./captcha/captcha_" + str(datetime.datetime.now().isoformat()) + ".png"
	else:
		captchaName = "./captcha/captcha_" + str(nameInfix) + ".png"

	return extractScreenPart(x-50, y+5, 170, 60, name=captchaName, debug=debug)
