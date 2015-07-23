class Global: # Global variable container
	version = '0.1b'

def bind(stdout, queue):
	for line in iter(stdout.readline, b''):
		queue.put(line)
	stdout.close()
