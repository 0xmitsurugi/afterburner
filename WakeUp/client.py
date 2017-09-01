#! /usr/bin/python
# coding: utf-8

import threading
import socket
import time
import datetime
import random
import struct

############ FILL WITH APPROPRIATE DATA ############
DEBUG=False
CC = "127.0.0.1"           #Put IP of C&C server
CCport = 6969              #Put port of C&C server
MHz='\x00\x02\x00\x00'     #Put MHz of the bot
UNAME='Linux router2 4.1.0-i386-pl12 #1 XcamSoft  4.1.0-i386-pl12 (2014-07-21) x86\n'                      #uname -a
IP='172.19.21.1'           #local IP address
############    END OF CONFIGURATION    ############

#Global vars
exitapp=False
sendstats=False

def matow(s):
    out=[]
    for i in range(len(s)):
        out.append(s[i]+'\x00')
    return ''.join(out)

REGISTER = MHz
REGISTER+= '\x00'*8   
REGISTER+= matow(UNAME)
padd=268-len(REGISTER)
REGISTER+= '\x00'*padd
REGISTER+= IP
padd=696-len(REGISTER)
REGISTER+= '\x00'*padd


def SendCpuMsg():
    """Register to botmaster, then send statistics"""
    server.send('\x01\x00\x01\x00'+REGISTER)
    while exitapp == False:
        time.sleep(5)
        cpu=random.randint(0,35)
        outrates=random.randint(0,255)
        if DEBUG and sendstats==True:
            print "[+] Debug: Sending stats"
        if sendstats == True:
            server.send('\x02\x00\x01\x00'+'\x00'*4+chr(outrates)+'\x00'*3+chr(cpu)+'\x00'*3)

def sendDoneMsg(timer):
    """ Used by bot when DDOS is finished """
    #This is not mandatory
    time.sleep(timer)
    msg='\x04\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x01'
    server.send(msg)

def rawprint(s):
    print "===== Raw DATA ====="
    print s.encode('hex')
    print "===== Raw DATA ====="
    
def prettyprint(s):
    atk=['attack_tcp_con','attack_tcp_slow','attack_tcp_syn/attack_udp_std','TODO','TODO','attack_http_get_slow','attack_http_get_spider','attack_http_post_flood','attack_http_post_slow']
    (attack,t1,t2,atk_type,dport,a,timer,delay,threads,size,f,g,h,i)=struct.unpack('<I268x128s256sIIIIIIIIIII',s[:700])
    if t2[0]=="\x00":
        t2="NONE"
    if atk_type < 9:
        print "[+] Attack type(%d): %s with %d thread(s)" % (atk_type,atk[atk_type], threads)
    else:
        print "[+] Attack type(%d): Unkown attack, new bot version? %d Thread(s)" % (atk_type,threads)
    print "    Targets: %s, %s; dport %d, duration %ds , delay %dms, size %d" % \
        (t1,t2,dport,timer,delay,size)
    print "    Other params: a: %d, f: %d, g: %d, h: %d, i: %d" % (a,f,g,h,i)

def parse_dos_cmd(data):
    """ Gives info about targets """
    if len(data) >= 700:
        prettyprint(data)
        #Don't forget to send back statistics when finished
        (attack,t1,t2,atk_type,dport,a,timer,delay,threads,size,f,g,h,i)=struct.unpack('<I268x128s256sIIIIIIIIIII',data[:700])
        threading.Thread(target=sendDoneMsg,args=(timer,)).start()
        if DEBUG==True:
            rawprint(data)
        return
    if len(data) < 700:
        print "[+] DEBUG : data %d bytes" % len(data)
        print "%s : Unknown DOS CMD, short packet!" % datetime.datetime.utcnow()
        rawprint(data)
        return

def parse_commands(data):
    global exitapp
    global sendstats
    """ Parse command from C&C, and log them """
    if data.startswith('\x04\x00\x01\x00'):
        #Never seen this command in the wild
        print "%s : DDos Halted" % datetime.datetime.utcnow()
    elif data.startswith('\x06\x00\x01\x00'):
        #Toggle True/False
        sendstats = not sendstats
        print "%s : Toggling sendstats: %s" % (datetime.datetime.utcnow(), sendstats)
    elif data.startswith('\x05\x00\x01\x00'):
        #105 is the way for botmaster to send commands
        if data[400:406] == 'exitse':
            """ Only seen in old versions """
            print "%s : Exit Self command" % datetime.datetime.utcnow()
            exitapp = True
            exit(0)
        elif data[400:406] == 'killse':
            """ Only seen in old versions """
            print "%s : Kill Self command" % datetime.datetime.utcnow()
            exitapp = True
            exit(0)
        elif data[400:406] == 'update':
            """ Only seen in old versions """
            URL=data[407:].split('\x00')[0]
            print "%s : Update URL: %s" % (datetime.datetime.utcnow(),URL)
        else:
            shellcmd=data[400:].split('\x00')[0]
            print "%s : Exec command: %s" % (datetime.datetime.utcnow(),shellcmd)
            #New versions doesn't send back results
            # Send a decoy to botmaster instead of exec()-ing commands ^^
            #msg ='*** glibc detected *** double free or corruption (out): 0xbfbdeae0 ***\n'
            #msg+='===== Stack Trace =====\n'
            #msg+='Aborting\n'
            #server.send('\x05\x00\x01\x00'+'\x00'*396+msg)
    elif data.startswith('\x03\x00\x01\x00'):
        print "[+] %s : DOS CMD" % (datetime.datetime.utcnow())
        parse_dos_cmd(data)
    else:
        print "%s : Unknown Command" % (datetime.datetime.utcnow())
        rawprint(data)


####### CONNECTING TO SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.connect((CC, CCport))
except:
    print "Cannot connect to the server %s:%d" % (CC, CCport)
    print "FATAL : Aborting"
    exit(0)

print "%s : Registering to server %s:%d" % (datetime.datetime.utcnow(), CC, CCport)

threading.Thread(target=SendCpuMsg).start()

#And now just listen for orders
while True:
    cmd = server.recv(1500)
    parse_commands(cmd)

