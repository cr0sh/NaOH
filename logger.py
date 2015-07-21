from screen.msgbox import Msgbox

def reportError(error, additional = '', title = '오류'):
	e = str(error)
	print('[NaOH Error] ' + e)
	e += additional
	Msgbox(e, title)
