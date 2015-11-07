usage = """
	-h, --help           For this output
	-k, --handleOK       Program handles false positives automatically
	-d, --debug          Output more information for debug purposes
	-r, --report         Specify an output directory for the reports
	-e, --explorer       Applies the tetragon detection on the specified report
	-l, --exploreLatest  Executes the explorer on the latest report
"""

prolog = """

AlphaBot v 0.1

Start your browser and access the alpha wars game.

Make sure that your base is completely displayed in the
browser window and that every base is clearly visible.

Ready for initialization...
"""

enter_to_continue = "Press enter to continue..."

move_mouse_to_browser = "Move your mouse into the browser window..."

fallback = """

Now click on a triangle of a capture and hit enter. This is needed to extract the position of the
OK button.
"""

initialization_done = "Initialization done!"

produce_fuel = "Produce fuel"

start_in = "Start in..."
