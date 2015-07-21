from tkinter import Tk, Frame, ttk
from os import path

class Screen:
	root = Tk()
	frame = ttk.Frame()
	def __init__(self):
		self.frames = list()
		print(str(Screen.root._w))
		Screen.root.call('wm', 'iconbitmap', Screen.root._w, '-default', path.join(path.dirname(path.dirname(path.realpath(__file__))), 'icon.ico'))
		Screen.root.iconbitmap(path.join(path.dirname(path.dirname(path.realpath(__file__))), 'icon.ico'))
		Screen.frame.destroy()
		Screen.frame=Frame(Screen.root)
		Screen.frame.pack(expand='false', padx=5, pady=5, fill='both')

	@staticmethod
	def title(title: str):
		Screen.root.title(title)

	def close(self):
		Screen.root.quit()

	def destroy(self):
		Screen.root.destroy()
