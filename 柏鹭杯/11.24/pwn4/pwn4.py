from pwn import *
p = remote('172.16.6.8',10003)

data = p.recvuntil('Hello')[:-5]
print data
d1 =u32(data[:4])
d2 =u32(data[4:8])
d3 = u32(data[8:])
log.info("d1:%#x,d1:%#x,d3:%#x",d1,d2,d3)

print p.recvuntil('2018!')
data = p.recvuntil('This')[:-4]
print data
d1 =u32(data[:4])
d2 =u32(data[4:8])
d3 = u32(data[8:12])
log.info("d1:%#x,d1:%#x,d3:%#x,other:%s",d1,d2,d3,data[12:])
p.interactive()
