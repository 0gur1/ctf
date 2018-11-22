from pwn import *
def h1(s):
	result = 4919;
	for c in s:
		result = result * ord(c)+1
	return result
def h2(s):
	result = 0
	i=0
	while i+1<len(s) and s[i] and s[i+1]  :
		tmp = ord(s[i+1])<<8 | ord(s[i])
		result ^= tmp
		i+=2
	if i<len(s) and s[i]:
		result ^= ord(s[i])
        return ((result>>10) ^ (result ^ (result >> 5))) &0x1f
def h3(s):
	result = 0
	for c in s:
		for i in range(8):
			if (ord(c)>>i)&1:
				result+=1;
		result&=0x1f;
	return result;
			
def brute1():
	for i in range(255,0,-1):
		print i
		for j in range(0,256):
			for k in range(0,256):
				for l in range(0,256):
					tmp = chr(i)+chr(j)+chr(k)+chr(l)
					if h1(tmp)%0x100000000 == 0x80000000:
						print tmp
						print "%d %d %d %d" %(i,j,k,l)
						return
def brute2():
	pos={}
	for i in range(0x1000000):
		tmp=p32(i)[:-1]
		#tmp+='\x00'

		a2=h2(tmp)
		a3=h3(tmp)
		
		if (abs(h1(tmp))%62)==60 and a2==a3:
			if not pos.has_key(a2):
				pos[a2]=1
				print "%d:%#x" %(a2,u32(tmp.ljust(4,'\x00')))			

brute2()


