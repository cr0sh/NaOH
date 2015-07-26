from threading import Thread

class Query:

	def __init__(self, stdin):
		self.replytable = []
		self.stdin = stdin

	def parse_reply(self, str):
		pass

	def communicate(self, querystr, callback):
		pass
