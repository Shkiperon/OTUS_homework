import os
import signal
import time
import sys

def sighup_handler(signal, frame):
	print("Stopping process. Reason is SIGHUP")
	sys.exit(1)

def sigint_handler(signal, frame):
	print("Stopping process. Reason is SIGINT")
	sys.exit(2)

def sigquit_handler(signal, frame):
	print("Stopping process. Reason is SIGQUIT")
	sys.exit(3)

def sigterm_handler(signal, frame):
	print("Stopping process. Reason is SIGTERM")
	sys.exit(15)

signal.signal(signal.SIGHUP, sighup_handler)
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGQUIT, sigquit_handler)
signal.signal(signal.SIGTERM, sigterm_handler)

print('Hello! I am an example')
pid = os.fork()
print('pid of my child is %s' % pid)
try:
	if pid == 0:
		print('I am a child. Im going to sleep')
		for i in range(1,40):
			print('mrrrrr')
			a = 2**i
			print(a)
			pid = os.fork()
			if pid == 0:
				print('my name is %s' % a)
				sys.exit(0)
			else:
				print("my child pid is %s" % pid)
			time.sleep(1)
		print('Bye')
		sys.exit(0)
	else:
		for i in range(1,200):
			print('HHHrrrrr')
			time.sleep(1)
			print(3**i)
		print('I am the parent')

except OSError:
	print ("System Error")

#pid, status = os.waitpid(pid, 0)
#print "wait returned, pid = %d, status = %d" % (pid, status)

