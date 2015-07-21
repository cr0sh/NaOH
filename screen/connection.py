from tkinter.ttk import Frame, Label, Button, Entry
from .screen import Screen
from .msgbox import Msgbox

class ConnectionScreen(Screen):
	def __init__(self, next):
		self.address = '127.0.0.1'
		self.port = 14333
		super().__init__()
		Screen.title('NaOH client')
		Screen.root.resizable(0, 0)
		master1 = Frame(Screen.root) # Master frame 1
		master1.pack(side='top')
		child1 = Frame(master1)
		child1.pack(side='left')
		lframe1 = Frame(child1)
		lframe1.pack()
		lframe2 = Frame(child1)
		lframe2.pack()
		Label(lframe1, text='서버 주소/포트: ', justify='right').pack(side='right', expand='true')
		Label(lframe2, text='        비밀번호: ', justify='right').pack(side='right', expand='true')
		child2 = Frame(master1)
		child2.pack(side='right')
		self.addrentry = Entry(child2)
		self.addrentry.insert(0, self.address + ':' + str(self.port))
		self.addrentry.pack()
		self.passwdentry = Entry(child2)
		self.passwdentry.insert(0, 'password')
		self.passwdentry.pack()
		master2 = Frame(Screen.root) # Master frame 2
		master2.pack(side='bottom')
		Button(master2.pack(), text='Connect', command=self.buttonPressed).pack(side='bottom')
		self.nextcallback = next

	def buttonPressed(self):
		if len(self.addrentry.get()) == 0:
			Msgbox('주소를 입력하세요', '오류', None)
			return

		if len(self.passwdentry.get()) == 0:
			Msgbox('비밀번호를 입력하세요', '오류', None)
			return

		temp = self.addrentry.get().split(':')
		error = False
		try:
			self.port = int(temp[1])
		except ValueError:
			error = True
		except IndexError:
			error = True

		if len(temp) != 2:
			error = True

		if error:
			Msgbox('주소는 IP(또는 도메인):포트 형식이여야 합니다.', '오류', lambda: self.entry.select_range(0, 'end'))
			return

		self.address = temp[0]
		self.nextcallback(self.address, self.port, self.passwdentry.get())
