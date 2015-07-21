from tkinter import Tk, Frame, ttk

class Screen:
	root = Tk()
	frame = ttk.Frame()
	def __init__(self):
		self.frames = list()
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
