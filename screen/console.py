import threading, sys, signal
from .screen import Screen
from .status import statusScreen
from .properties import propertiesScreen
from tkinter.ttk import *
from tkinter import Listbox, Frame
from os import read, write, unlink, kill, getpid, sep, listdir, path
from .msgbox import Msgbox
from time import sleep

def asyncStream(scr):
	sid = None
	try:
		while True:
			for line in iter(scr.runner.pipe.stdout.readline, b''):
				buf = line.decode("utf-8")
				if buf[:7] == '* NaOH ':
					scr.messages[buf[7:11]] = buf[12:]
					continue

				scr.listbox.insert('end', buf + '\n')
				if not scr.scrolllock:
					scr.listbox.yview('end')

			scr.listbox.insert('end', '[!] 서버가 정지되었습니다\n')
			scr.listbox.yview('end')
			break

	except RuntimeError as e:
		print('Fatal error on async streaming thread: ' + str(e))
		print('Shutting down NaOH')
		kill(scr.runner.pipe.pid, signal.SIGTERM)
		return


class consoleScreen(Screen):

	def __init__(self, runner):
		self.runner = runner
		self.messages = {}
		Screen.destroy()
		Screen.reinit()
		super().__init__()
		Screen.title("NaOH: PocketMine-MP Console")

		# GUI initialization

		fstframe = Frame(Screen.root)
		fstframe.grid(row=0, rowspan=1, columnspan=8)
		sndframe = Frame(Screen.root)
		sndframe.grid(row=0, rowspan=1, column=8, columnspan=2)
		self.scrollbar = Scrollbar(fstframe)
		self.listbox = Listbox(fstframe, yscrollcommand=self.scrollbar.set, width=120, height=25)
		self.listbox.grid(row=0, column=0, rowspan=1, columnspan=7, sticky='nswe')
		self.scrollbar.config(command=self.listbox.yview)
		self.scrollbar.grid(row=0, column=7, rowspan=1, sticky='nse')
		self.scrolllock = False
		Button(fstframe, text='나가기 (주의: 강제 종료됩니다)', command=self.runner.killAll).grid(row=1, column=0, sticky='nwse')
		self.slbutton = Button(fstframe, text='ScrollLock Off', command=self.togglesl)
		self.slbutton.grid(row=1, column=1, sticky='new')
		Label(fstframe, text='명령어: /', justify='right').grid(row=1, column=2)
		self.cmdentry = Entry(fstframe)
		self.cmdentry.bind('<Return>', self.put_cmd)
		self.cmdentry.grid(row=1, column=3, columnspan=5, sticky='nwe')
		fstframe.rowconfigure(1, weight=1)
		fstframe.columnconfigure(3, weight=1)
		fstframe.columnconfigure(4, weight=20)
		sndframe.rowconfigure(0, weight=1)
		Button(sndframe, text='서버 상태', command=lambda: statusScreen(self)).grid(row=0, sticky='n')
		Button(sndframe, text='설정 편집', command=lambda: propertiesScreen(self.runner.workdir + sep + 'server.properties')).grid(row=1, sticky='n')
		Button(sndframe, text='덤프 삭제', command=self.removeDumps).grid(row=2, sticky='n')
		self.cmdentry.focus()
		Screen.root.focus_force()

		# GUI initialization done

		self.thread = threading.Thread(target=lambda: asyncStream(self)).start()
		Screen.root.protocol("WM_DELETE_WINDOW", self.runner.killAll)
		Screen.root.mainloop()
		try:
			Screen.root.destroy()
		except:
			self.runner.killAll()

	def put_cmd(self, event):
		# self.runner.pipe.communicate(('/' + self.cmdentry.get() + '\n').encode(), timeout=0)
		write(self.runner.pipe.stdin.fileno(), (self.cmdentry.get() + '\n').encode('utf-8'))
		self.cmdentry.delete(0, 'end')

	def togglesl(self):
		if self.scrolllock:
			self.scrolllock = False
			self.slbutton['text'] = 'ScrollLock Off'
		else:
			self.scrolllock = True
			self.slbutton['text'] = 'ScrollLock On'

	def removeDumps(self):
		files = [f for f in listdir(self.runner.workdir) if path.isfile(path.join(self.runner.workdir, f)) and f[0:9] =='CrashDump']
		for f in files:
			unlink(path.join(self.runner.workdir, f))

		self.listbox.insert('end', '')
		if len(files) > 0:
			self.listbox.insert('end', '** %d개의 크래시 덤프들이 삭제되었습니다' % len(files))
		else:
			self.listbox.insert('end', '** 삭제할 크래시 덤프가 없습니다.')
		self.listbox.insert('end', '')
		if not self.scrolllock:
			self.listbox.yview('end')
