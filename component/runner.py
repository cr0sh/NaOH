import sys, os, time, global_var, atexit, signal, queue
from subprocess import PIPE, Popen
from threading import Thread
from screen.msgbox import Msgbox
from screen.console import consoleScreen

class Runner:
	def __init__(self, runtime, code, workdir):
		block = False
		if not os.path.isfile(runtime.replace(r"\\", r"\\\\")) or not os.path.isfile(code.replace(r"\\", r"\\\\")):
			block = True
			Msgbox("지정한 파일을 찾을 수 없습니다: \n%s\n%s" % (runtime.replace(r"\\", r"\\\\"), code.replace(r"\\", r"\\\\")), "오류", lambda: sys.exit(1))

		if not block:
			self.runtime = runtime
			self.target = code
			posix = 'posix' in sys.builtin_module_names
			self.pipe = Popen([runtime, code], cwd=workdir, stdout=PIPE, bufsize=1, close_fds=posix)
			self.queue = queue.Queue()
			self.async = Thread(target=global_var.bind, args=(self.pipe.stdout, self.queue))
			self.async.daemon = True
			self.async.start()
			atexit.register(lambda: os.kill(self.pipe.pid, signal.SIGTERM))
			consoleScreen(self)

"""
	def __getstate__(self):
		state = self.__dict__.copy()
		del state['namelist']
		return state

	def __setstate__(self, state):
		self.__dict__.update(state)
"""
