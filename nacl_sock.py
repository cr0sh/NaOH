from socket import *
from time import *
from screen import msgbox
import logger

class Nacl_sock:
	def __init__(self, address, port):
		self.working = False
		try:
			self.socket = socket(AF_INET, SOCK_STREAM)
			self.socket.connect((address, port))
			self.working = True
		except ConnectionRefusedError as e:
			logger.reportError(e, '\n\n연결에 실패했습니다(Tip: 서버에 HCl이 설치되어 있는지 확인하세요)')

	def recv(self, timeout=2):
		self.socket.setblocking(False)
		total_data = []
		data = ''
		begin = time()

		while True:
			if total_data and time() - begin > timeout:
				break
			elif time() - begin > timeout * 2:
				break

			try:
				data = self.socket.recv(4096)
				if data:
					total_data.append(data)
					begin=time()
				else:
					sleep(0.1)
			except:
				pass

		return ''.join(total_data)

	def send(self, payload):
		self.socket.sendall(str(len(payload.split(' ')[0])) + payload)

	def close(self):
		self.socket.close()
		self.working = False
