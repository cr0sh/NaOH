from threading import Thread

class Query:

	def __init__(self, stdin):
		self.replytable = []
		self.lock = False
		self.stdin = stdin

	def parse_reply(self, str):
		self.lock = True
		lines = str.split('\n')
		replyid = int(lines[0][1:])
		if not replyid in self.replytable:
			self.replytable[id] = []
		for line in lines[1:]
			if line != '*end ' + replyid:
				break
			self.replytable[replyid].append(line)
		self.lock = False


	def communicate(self, pipe, querystr, callback):


	def listenon(self, timeout, callback):
