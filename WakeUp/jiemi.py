#! /usr/bin/python
# This program implements the jiemi obfuscation

import sys

if len(sys.argv) < 2:
    print "[ ] Give a string"
    exit(1)

cipher=sys.argv[1]
print "[+] Decoding %s" % cipher

#Very secure Key
key=[-1,1,2]
sol=[]

for i in range(len(cipher)):
    sol.append(chr(ord(cipher[i])+key[i%3]))

print "[+] Clear text: %s" % ''.join(sol)
