import sys
import os
import string
import tetragonDetector

time = None
bgLayer = None
captcha = None
prcCaptcha = None
x_target = None
y_target = None


def readReport(filePath, debug=False):
	global time, bgLayer, captcha, prcCaptcha, x_target, y_target 

	f = open(filePath, "r")

	for line in f:
		if "Time:" in line:
			time = line[5:].strip()
		if "backgroundlayer:" in line:
			bgLayer = line[16:].strip()
		if "captchaPath:" in line:
			captcha = line[12:].strip()
		if "processedImage:" in line:
			prcCaptcha = line[15:].strip()
		if "x_target:" in line:
			value = line[9:]
			if not "None" in value:
				x_target = float(value)
		if "y_target:" in line:
			value = line[9:]
			if not "None" in value:
				y_target = float(value)

	f.close()

	if debug:
		print "File: " + str(filePath)
		print "Time: " + str(time)
		print "Background Layer: " + str(bgLayer)
		print "Captcha: " + str(captcha)
		print "Processed captcha: " + str(prcCaptcha)
		print "x_target: " + str(x_target)
		print "y_target: " + str(y_target)

def showImageProcessing():
	print "Executing:"
	print "print str(findTetragonLineBased(\"" + str(captcha) + "\", backgroundLayerPath=\"" + str(bgLayer) + "\", report=None, _debug=True))"
	tetragonDetector.findTetragonLineBased(captcha, report=None, backgroundLayerPath=bgLayer, _debug=True)


def analyseReport(filePath=None):
	"""
	Analyses the given report
	If no file path is given it searchs for the latest report in the standard
	report directory
	"""
	if None == filePath:
		all_subdirs = ["./reports/" + d for d in os.listdir("./reports") if os.path.isdir("./reports/" + d)]
		latest_subdir = max(all_subdirs, key=os.path.getmtime)
		all_subFiles = [latest_subdir + "/" + d for d in os.listdir(latest_subdir) if os.path.isfile(latest_subdir + "/" + d)]
		latest_file = max(all_subFiles, key=os.path.getmtime)
		filePath = latest_file

	readReport(filePath, True)
	showImageProcessing()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		analyseReport(sys.argv[1])
	else:
		analyseReport(None)
