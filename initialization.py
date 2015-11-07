import mapExtractor
import english
import alphaBotUtility

def initializeFactoryPosition():
	"""
	Contains the in/output of the factory initialization
	"""
	print english.move_mouse_to_browser 

	alphaBotUtility.countDownwards(5)

	alphaBotUtility.showSpinner()

	mapExtractor.initialize()

	alphaBotUtility.hideSpinner()

def initializeOKPosition():
	"""
	Contains the in/output of the OK initialization
	"""
	print english.fallback

	raw_input(english.enter_to_continue)
	print english.move_mouse_to_browser
	alphaBotUtility.countDownwards(5)

	alphaBotUtility.showSpinner()

	mapExtractor.initializeOK()

	alphaBotUtility.hideSpinner()

def initialize(handleOK=False):
	"""
	Does the whole initialization
	"""
	print english.prolog
	raw_input(english.enter_to_continue)

	initializeFactoryPosition()

	if handleOK:
		initializeOKPosition()

	print english.initialization_done
	raw_input(english.enter_to_continue)
