from .screen import Screen
from .msgbox import Msgbox
from global_var import Global
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askdirectory
from os import path, unlink
from sys import exit
import json, logger
from .console import consoleScreen
from component.runner import Runner

class launcherScreen(Screen):

	def __init__(self):
		self.runtime = ''
		self.target = ''
		self.workdir = ''
		cfg = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'config.json')
		global js
		if path.isfile(cfg):
			try:
				cfg_f = open(cfg, 'r')
				js = json.loads(cfg_f.read())
				cfg_f.close()
				loaded = True
			except ValueError:
				cfg_f.close()
				unlink(cfg)
				loaded = False
		else:
			loaded = False
		Screen.close()
		# Screen.reinit()
		super().__init__()
		Screen.title('NaOH launcher')
		Screen.root.resizable(0, 0)
		master = Frame(Screen.root) # Master frame
		master.pack(side='top')
		Label(master, text='NaOH launcher (version %s)' % str(Global.version), justify='center').grid(row=0, columnspan=3, padx=(100, 100))
		Label(master, text='PHP 바이너리 파일: ').grid(row=1, sticky='e')
		Label(master, text='PocketMine-MP: ').grid(row=2, sticky='e')
		Label(master, text='작업 폴더: ').grid(row=3, sticky='e')
		self.runtimeentry = Entry(master)
		self.runtimeentry.grid(row=1, column=1)
		self.targetentry = Entry(master)
		self.targetentry.grid(row=2, column=1)
		self.cwdentry = Entry(master)
		self.cwdentry.grid(row=3, column=1)
		if loaded:
			try:
				self.runtimeentry.insert(0, js['runtime_file'])
				self.targetentry.insert(0, js['pocketmine_code'])
				self.cwdentry.insert(0, js['working_dir'])
			except KeyError as ex:
				Msgbox(str(ex))
				logger.reportError(ex, '파일이 손상된 것 같습니다. 계속 오류가 발생하면 config.json을 지워주세요')

		Button(master, text='설정', command=self.chooseRuntime).grid(row=1, column=2, sticky='w')
		Button(master, text='설정', command=self.chooseTarget).grid(row=2, column=2, sticky='w')
		Button(master, text='설정', command=self.chooseCwd).grid(row=3, column=2, sticky='w')
		Button(master, text='시작!', command=self.start).grid(row=4, column=0, columnspan=2)
		Button(master, text='취소', command=lambda: exit(0)).grid(row=4, column=1, columnspan=2)

	def chooseRuntime(self):
		tmp = askopenfilename(parent=Screen.root, title='PHP 파일을 선택하세요')
		if len(tmp) < 3 or tmp[-3:len(tmp)] != 'exe':
			Msgbox('제대로 된 실행 파일이 아닌 것 같습니다. PocketMine-MP가 제대로 구동되지 않을 수 있습니다.')
		self.runtimeentry.delete(0, 'end')
		self.runtimeentry.insert(0, tmp)

	def chooseTarget(self):
		tmp = askopenfilename(parent=Screen.root, title='PocketMine-MP 코드를 선택하세요')
		if len(tmp) < 3 or (tmp[-3:len(tmp)] != 'php' and tmp[-4:len(tmp)] != 'phar'):
			Msgbox('제대로 된 PocketMine-MP 파일이 아닌 것 같습니다. PocketMine-MP가 제대로 구동되지 않을 수 있습니다.')
		self.targetentry.delete(0, 'end')
		self.targetentry.insert(0, tmp)

	def chooseCwd(self):
		tmp = askdirectory(parent=Screen.root, title='작업 경로를 설정하세요')
		self.cwdentry.delete(0, 'end')
		self.cwdentry.insert(0, tmp)

	def start(self):
		with open(path.join(path.dirname(path.dirname(path.realpath(__file__))), 'config.json'), 'w+') as js:
			json.dump({'runtime_file': self.runtimeentry.get(), 'pocketmine_code': self.targetentry.get(), 'working_dir': self.cwdentry.get()}, js)
		self.runner = Runner(self.runtimeentry.get(), self.targetentry.get(), self.cwdentry.get())
