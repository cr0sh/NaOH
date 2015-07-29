from tkinter.ttk import *
from screen import *
from screen.splash import splashScreen
from time import sleep
from screen.console import consoleScreen
from screen.launcher import launcherScreen

def init():
	splashScreen(1500)
	launcherScreen()
	screen.Screen.root.mainloop()

if __name__ == '__main__':
		init()

# with splashScreen('splash.gif'):
# 	time.sleep(4)

# screen.Screen.root.mainloop()
