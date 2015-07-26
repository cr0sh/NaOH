from tkinter import Tk, Frame, ttk
from os import path

class Screen:
	root = Tk()
	frame = ttk.Frame()
	def __init__(self):
		self.frames = list()
		Screen.root.call('wm', 'iconbitmap', Screen.root._w, '-default', path.join(path.dirname(path.dirname(path.realpath(__file__))), 'icon.ico'))
		Screen.root.resizable(0, 0)
		Screen.root.iconbitmap(path.join(path.dirname(path.dirname(path.realpath(__file__))), 'icon.ico'))
		Screen.frame.destroy()
		Screen.frame=Frame(Screen.root)
		# Screen.frame.pack(expand='false', padx=5, pady=5, fill='both')

	@staticmethod
	def title(title: str):
		Screen.root.title(title)

	@staticmethod
	def close():
		Screen.root.quit()

	@staticmethod
	def destroy():
		Screen.root.destroy()

	@staticmethod
	def reinit():
		Screen.root = Tk()
		Screen.frame = ttk.Frame()
