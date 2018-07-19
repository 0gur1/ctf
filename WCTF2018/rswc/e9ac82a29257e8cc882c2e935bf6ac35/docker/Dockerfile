FROM ubuntu:16.04

ADD rswc /tmp/rswc
ADD flag.txt /tmp/flag.txt
ADD launch.sh /tmp/launch.sh
ADD xinetd /tmp/xinetd

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y xinetd && \
    useradd -m chall && \
    useradd user && \
    mv /tmp/xinetd /etc/xinetd.d/rswc && \
    mv /tmp/rswc /home/chall && \
    mv /tmp/launch.sh /home/chall && \
    chown -R root:root /home/chall && \
    chown root:chall /home/chall/rswc && \
    chmod 2755 /home/chall/rswc && \
    chmod 755 /home/chall/launch.sh && \
    mv /tmp/flag.txt /home/chall && \
    chown root:chall /home/chall/flag.txt && \
    chmod 440 /home/chall/flag.txt && \
    perl -e 'print "\0" x 0x4000' >> /etc/ld.so.cache  # I know this is weird but we need enough space to make my allocator works properly :P

CMD touch /root/xinetd.log && service xinetd start && tail -f /root/xinetd.log
