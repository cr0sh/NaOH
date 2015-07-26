from tkinter import Tk
from tkinter.ttk import *
from .screen import Screen

class Msgbox:
	def __init__(self, message, title='알림', callback=None):
		tk=Tk()
		tk.resizable(0, 0)
		self.frame = Frame(tk, border=7)
		self.frame.pack(expand='true')
		self.frame.master.title(title)
		Label(self.frame, text=message).pack(side='top', expand='true')
		self.callback=callback
		Button(self.frame, text="확인", command=self.onPress).pack(expand='true')
		tk.focus_force()

	def onPress(self):
		if self.callback != None:
			self.callback()

		self.frame.master.destroy()
