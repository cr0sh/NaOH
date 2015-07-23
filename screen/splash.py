from tkinter import *
from os import path

class splashScreen:
	def __init__(self, img):
		self.working = True
		self.root = Tk()
		self.root.overrideredirect(True)
		self.width = 515
		self.height = 250
		self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, self.width, self.height))
		self.image_file = path.join(path.dirname(path.dirname(path.realpath(__file__))), img)
		self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

	def __enter__(self):
		canvas = Canvas(self.root, height=self.height, width=self.width, bg="brown")
		image = PhotoImage(master = canvas, height=self.height, width=self.width, file=self.image_file)
		canvas.create_image(self.width/2, self.height/2, image=image)
		canvas.pack()
		# show the splash screen for 5000 milliseconds then destroy\
		self.root.mainloop()

	def on_quit(self):
		self.__exit__()

	def __exit__(self, *args):
		if self.working:
			self.root.destroy()
			self.working = False
