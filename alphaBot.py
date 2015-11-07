import alphaBotUtility

import os
import sys
import getopt

import english
import initialization
import bot
import report
import reportExplorer

handleOK = False 
debug = False 

try:
	opts, args = getopt.getopt(sys.argv[1:], "hkdr:e:l", ["help", "handleOK", "debug", "report", "explorer", "exploreLatest"])
except getopt.GetoptError as err:
	print str(err)
	usage()
	sys.exit(2)

verbose = False
for o, a in opts:
	if o == "-v":
		verbose = True
	elif o in ("-h", "--help"):
		alphaBotUtility.usage()
		sys.exit()
	elif o in ("-k", "--handleOK"):
		handleOK = True
	elif o in ("-d", "--debug"):
		debug = True
	elif o in ("-r", "--report"):
		report.reportDirectory = str(a)
	elif o in ("-e", "--explorer"):
		report = str(a)
		reportExplorer.analyseReport(report)
		sys.exit()
	elif o in ("-l", "--exploreLatest"):
		reportExplorer.analyseReport(None)
		sys.exit()
	else:
		assert False, "unhandled option"

captchaDir = "./captcha"
if not os.path.exists(captchaDir):
    os.makedirs(captchaDir)

initialization.initialize(handleOK=handleOK)

bot.run(handleOK=handleOK, debug=debug)
