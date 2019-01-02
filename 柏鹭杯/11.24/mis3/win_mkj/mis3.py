s=''
for i in range(1000,2321):
	name = str(i)+'.txt'
	f = open(name)
	c = f.read(1)
	s+=c
	f.close()
print s
