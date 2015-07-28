from .independentScreen import independentScreen
from tkinter.ttk import *
from tkinter import Label, StringVar, Tk
from threading import Thread
from time import sleep
import sys

class statusScreen(independentScreen):

	working = False

	def __init__(self, owner):
		if super().__init__() == False:
			return

		self.owner = owner
		self.root.title('정보')
		self.label = Label(self.root, text='서버 상태 읽는 중...\n\n(계속 나타나지 않으면 서버에 HCl이 설치되어 있나 확인하세요)', justify='center')
		self.label.grid(row=0, column=0)
		Button(self.root, text='나가기', command=self.quit).grid(row=1, column=0, sticky='nwe')
		self.thread = Thread(target=self.updateThread)
		statusScreen.working = True
		self.thread.start()
		self.root.mainloop()

	def updateThread(self):
		while True:
			if not self._available():
				self.quit()
				break

			try:
				self.label['text'] = ('메인 스레드 메모리 사용량: %s\n최대 메모리: %s\n최대 가상 메모리: %s\n힙 메모리: %s\n서버 구동 시간: %s\n업로드 속도: %s\n다운로드 속도: %s\n플레이어 수/최대 플레이어 수: %s' % tuple(self.owner.messages['stat'].split(';')))
			except:
				sleep(1)

			sleep(1)

		sys.exit(0)
