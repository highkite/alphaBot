import threading
import sys
from time import sleep

import english

def countDownwards(i):
	"""
	Shows a counter in the command line
	"""
	while i > 0:
		sys.stdout.write("\r" + str(i) + " seconds")
		sys.stdout.flush()
		sleep(1)
		i -= 1

def spinnerThread(arg, stopEvent):
	"""
	Shows a spinner in the command line
	"""
	while not stopEvent.is_set():
		sys.stdout.write("\r-")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r\\")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r|")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r/")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r-")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r\\")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r|")
		sys.stdout.flush()
		stopEvent.wait(1)
		sys.stdout.write("\r/")
		sys.stdout.flush()
		stopEvent.wait(1)

stopEvent = None
thread = None

def showSpinner():
	"""
	Starts the spinner thread
	"""
	global stopEvent
	global thread

	stopEvent = threading.Event()
	thread = threading.Thread(target=spinnerThread, args=(1, stopEvent))
	thread.start()

def hideSpinner():
	"""
	Stops the spinner thread
	"""
	global stopEvent
	global thread

	stopEvent.set()
	thread.join()

def usage():
	"""
	Prints usage for alphabot
	"""
	print english.usage
