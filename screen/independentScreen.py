from tkinter import Tk

class independentScreen():
	screenDict = {}
	def __init__(self):
		if self._available():
			self.quit()
			return False

		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.quit)
		self.root.resizable(0, 0)
		self.root.focus_force()
		independentScreen.screenDict[self._name()] = self

	def _name(self):
		return self.__class__.__name__

	def _available(self):
		return self._name() in independentScreen.screenDict and isinstance(independentScreen.screenDict[self._name()], type(self))

	def quit(self):
		try:
			independentScreen.screenDict[self._name()].root.destroy()
			del independentScreen.screenDict[self._name()]
		except:
			pass
