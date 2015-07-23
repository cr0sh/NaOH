import threading
from .screen import Screen
from tkinter.ttk import *
from tkinter import Listbox

class consoleScreen(Screen):

	def __init__(self, runner):
		self.runner = runner
		super().__init__()
		self.scrollbar = Scrollbar(Screen.root)
		self.scrollbar.pack(side='right', fill='y')
		self.listbox = Listbox(Screen.root)
		self.listbox.pack()
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)
		threading.Thread(target=self.synchronizedStream, args=(self.listbox, self.runner.queue))

	def synchronizedStream(listbox, queue):
		while True:
			# listbox.insert('end', queue.get())
			print(queue.get()) # ONLY FOR DEBUGGING
