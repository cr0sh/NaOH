from tkinter.ttk import *
from screen import *
from nacl_sock import Nacl_sock

cnts = sock = None

def connect(addr, port, passwd):
	global sock
	if sock != None:
		sock.close()

	sock = Nacl_sock(addr, port)
	if not sock.working:
		return
	sock.send('CONNECT ' + passwd)
	response = sock.recv()
	if response != 'ACCEPTED':
		msgbox.Msgbox('HCl 서버에서 연결을 거부했습니다.\n\n(Tip: 비밀번호를 정확히 입력하셨나요?)')

cnts = connection.ConnectionScreen(connect)
screen.Screen.root.mainloop()
