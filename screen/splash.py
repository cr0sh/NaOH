from tkinter import *
from os import path
from time import sleep

class splashScreen:
	def __init__(self, delay):
		self.root = Tk()
		self.root.withdraw()
		window = Toplevel(self.root)
		canvas = Canvas(window)
		splash = PhotoImage(master=window, file= path.join(path.dirname(path.dirname(path.realpath(__file__))), 'splash.gif'))
		scrW = window.winfo_screenwidth()
		scrH = window.winfo_screenheight()
		imgW = splash.width()
		imgH = splash.height()
		Xpos = (scrW - imgW) // 2
		Ypos = (scrH - imgH) // 2
		window.overrideredirect(True)
		window.geometry('+{}+{}'.format(Xpos, Ypos))
		canvas.configure(width=imgW, height=imgH, highlightthickness=0)
		canvas.grid()
		canvas.create_image(imgW // 2, imgH // 2, image=splash)
		window.update()
		sleep(delay / 1000)
		self.root.destroy()
