import sys, os, time, global_var, signal
from multiprocessing import Queue
from subprocess import PIPE, Popen, STARTUPINFO, STARTF_USESHOWWINDOW
from threading import Thread
from screen.msgbox import Msgbox
from screen.console import consoleScreen

def bind(stdout, queue):
	for line in iter(stdout.readline, b''):
		# print(line) # DEBUGGING CODE
		queue.put(line)
	stdout.close()

class Runner:
	def __init__(self, runtime, code, workdir):
		self.workdir = workdir
		self.launch(runtime, code, workdir)
		consoleScreen(self)

	def launch(self, runtime, code, workdir):
		block = False
		if not os.path.isfile(runtime.replace(r"\\", r"\\\\")) or not os.path.isfile(code.replace(r"\\", r"\\\\")):
			block = True
			Msgbox("지정한 파일 또는 경로를 찾을 수 없습니다.", "오류", lambda: sys.exit(1))

		if not block:
			self.runtime = runtime
			self.target = code
			posix = 'posix' in sys.builtin_module_names
			si = STARTUPINFO()
			si.dwFlags |= STARTF_USESHOWWINDOW
			self.pipe = Popen([runtime, code], cwd=workdir, stdout=PIPE, stdin=PIPE, bufsize=1, close_fds=posix, startupinfo=si)

	def close(self):
		try:
			self.pipe.stdout.close()
			self.pipe.stdin.close()
		except:
			pass

	def killAll(self):
		try:
			os.kill(self.pipe.pid, signal.SIGTERM)
		except:
			pass

		os.kill(os.getpid(), signal.SIGTERM)
