string = "This is a standard test string."
a = ''.join(format(ord(i),'b').zfill(8) for i in string)

print(str(len(a)))

mystr = ""

for i in range(len(a)//8):
    mystr += chr(int(a[i*8:i*8+8], 2))

print(mystr)
