import time, sys, termios, fcntl, struct, signal

class sierpi(object):
	def __init__(self):
		self.c = '#'
		self.n = ' '
		self.startPos = int(self.getWidth()/2)
		self.terminalWidth = self.getWidth()
		if len(sys.argv) == 2:
			self.terminalWidth = int(sys.argv[1])
		self.wait = 0.05

		self.line = [v for v in self.n*self.terminalWidth]
		for i in range(len(self.line)):
			if i == self.startPos:
				self.line[i] = self.c

		signal.signal(signal.SIGWINCH, self.onResize)

	def num(self, what, l):
		num = 0
		for i in l:
			if i == what:
				num += 1
		return num

	def genNextLine(self):
		nextLine = [v for v in self.n*self.terminalWidth]
		tripple = []

		for i in range(len(self.line)):
			try:
				tripple = [self.line[i-1], self.line[i], self.line[i+1]]
			except IndexError:
				tripple = [self.line[i-1], self.line[i], self.n]
			if self.num(self.c, tripple) == 1:
				try:
					nextLine[i] = self.c
				except IndexError:
					pass

		return nextLine

	def getWidth(self):
		s = struct.pack("HHHH", 0, 0, 0, 0)
		fd_stdout = sys.stdout.fileno()
		x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
		return struct.unpack("HHHH", x)[1] # [1] -> Columns

	def onResize(self, signum, frame):
		self.terminalWidth = self.getWidth()

	def runner(self):
		while True:
			cur = ''.join(self.line)
			print(cur)
			self.line = self.genNextLine()
			time.sleep(self.wait)

sierpi().runner()
