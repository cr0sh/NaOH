from .independentScreen import independentScreen
from tkinter.ttk import *
from tkinter import Label, Tk
from collections import OrderedDict
from .msgbox import Msgbox

class propertiesScreen(independentScreen):
	hint = {
		'allow-flight': '서바이벌 날기 모드를 허용하면 on으로 설정합니다.',
		'announce-player-achievements': '플레이어가 업적을 달성하면 알림을 공개적으로 표시하려면 on으로 설정합니다.',
		'auto-save': '주기적으로 월드를 자동 저장하려면 on으로 설정합니다.',
		'enable-query': 'UT3 Query 프로토콜을 활성화하려면 on으로 설정합니다. 비활성화하면 외부에서 서버 상태를 알 수 없습니다.',
		'enable-rcon': 'Source RCON(원격 제어) 프로토콜을 활성화하려면 on으로 설정합니다. 서버 원격 제어 소프트웨어를 사용하려면 활성화해야 합니다.',
		'gamemode': '0 = 서바이벌, 1 = 크리에이티브',
		'generator-settings': '월드 생성기 설정입니다. 사용하는 level-type 설정에 따라 필요할 수도 있고 아닐 수도 있습니다.',
		'hardcore': '하드코어 모드를 활성화하려면 on으로 설정합니다.',
		'level-name': '서버에서 기본적으로 불러올 월드 폴더 이름을 설정합니다.',
		'level-seed': '월드 생성에 사용할 시드입니다.',
		'level-type': '생성할 월드의 유형입니다. FLAT으로 설정하면 평지맵, DEFAULT로 설정하면 MCPE 바이옴이 됩니다.',
		'max-players': '서버에 입장할 수 있는 최대 플레이어 수입니다.',
		'motd': '서버 접속 시 플레이어에게 보낼 문구입니다. @player 문자는 자동으로 매번 접속한 플레이어 닉네임이 됩니다.',
		'pvp': '플레이어들끼리 공격할 수 있게 하려면 on으로 설정합니다.',
		'rcon.password': 'RCON 프로토콜 접속 비밀번호입니다. 보안을 위해 강력한 비밀번호를 사용하기를 권장합니다.',
		'server-port': '서버 포트입니다. MCPE에서 기본으로 탐색하는 로컬 멀티플레이 포트는 19132입니다.',
		'spawn-protection': '스폰 지점에서 몇 블럭만큼의 거리가 부서지지 않도록 보호할 지 결정합니다. OP는 제한되지 않습니다.'
	}
	def __init__(self, filedir):
		if super().__init__() == False:
			return

		self.root.title('설정')
		self.root.resizable(1, 0)
		self.label = Label(self.root, text='서버 설정 읽는 중...')
		self.label.grid(row=0, column=0)
		Button(self.root, text='나가기', command=self._quit).grid(row=1, column=0, sticky='nwe')
		self.filedir = filedir
		f = open(self.filedir, 'r')
		self.lines = f.readlines()
		f.close()
		self.label['text'] = ''
		self.label['justify'] = 'left'
		self.properties = {}
		for line in self.lines:
			tmp = line[:len(line) - 1]
			if tmp[0] == '#':
				continue

			splitz = tmp.split('=', 1)
			self.properties[splitz[0]] = splitz[1]

		self.table = Treeview(self.root, selectmode='browse', columns=('c1', 'c2', 'c3'), show='headings')
		self.table.column('c1', width=200)
		self.table.column('c2', width=110)
		self.table.column('c3', width=550)
		self.table.heading('c1', text='이름')
		self.table.heading('c2', text='값')
		self.table.heading('c3', text='설명')
		self.properties = OrderedDict(sorted(self.properties.items()))
		for key, value in self.properties.items():
			if key in propertiesScreen.hint:
				self.table.insert('', 'end', text='', values=(key, value, propertiesScreen.hint[key]))
				continue

			self.table.insert('', 'end', text='', values=(key, value, ''))
		self.table.grid(row=0, column=0, sticky='nwe')
		self.table.bind('<Double-1>', self.edit_properties)
		self.root.columnconfigure(0, weight=1)
		self.root.mainloop()

	def binder(self, *args):
		self.set_properties(self.key['text'], self.valueEntry.get())

	def edit_properties(self, dummy):
		(key, value, description) = self.table.item(self.table.selection()[0])['values']
		self.window = Tk()
		self.window.grab_set_global()
		self.valueEntry = Entry(self.window)
		self.valueEntry.insert(0, value)
		Label(self.window, text=key + ': ', justify='right').grid(row=0, column=0, sticky='ne')
		self.valueEntry.grid(row=0, column=1, columnspan=3, sticky='nwe')
		self.valueEntry.focus_force()
		# self.valueEntry.bind('<Enter>', self.binder)
		self.key = Label(self.window, text=description.replace('. ', '.\n'), justify='left')
		self.key.grid(row=1, column=0, columnspan=4,sticky='news')
		Button(self.window, text='저장', command=lambda: self.set_properties(key, self.valueEntry.get())).grid(row=2, column=0, columnspan=4, sticky='new')
		self.window.mainloop()

	def set_properties(self, key, value):
		self.properties[key] = value
		self.window.destroy()
		del self.window
		del self.valueEntry
		del self.key
		self.save_and_refresh()

	def save_and_refresh(self):
		for num, line in enumerate(self.lines):
			lst = line[:len(line) - 1].split('=')
			if len(lst) < 2:
				continue

			if lst[1] != self.properties[lst[0]]:
				self.lines[num] = lst[0] + '=' + self.properties[lst[0]] + '\n'

		buf = ''
		for line in self.lines:
			buf += line

		f = open(self.filedir, 'w')
		f.write(buf)
		f.close()

		for t in self.table.get_children():
			self.table.delete(t)

		self.properties = OrderedDict(sorted(self.properties.items()))
		for key, value in self.properties.items():
			if key in propertiesScreen.hint:
				self.table.insert('', 'end', text='', values=(key, value, propertiesScreen.hint[key]))
				continue

			self.table.insert('', 'end', text='', values=(key, value, ''))

	def _quit(self):
		Msgbox('설정을 편집한 후에는 서버를 재시작하셔야 저장됩니다', '알림', None, True)
		self.quit()
