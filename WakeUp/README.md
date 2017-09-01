# WakeUp
This is the python client of the malware reversed here http://0x90909090.blogspot.fr/2017/08/meet-wake-malware-ddos-and-more.html

Another blogpost will cover an updated version of this malware.

**Warning**: if you connect to a C&C, the botmaster will know you IP address (obviously). Be concerned that the botmaster has control of a DDOS botnet which could harm you (or yout internet connection) a lot. Use at your own risk!

## Files
 * client.py : This is the client used to connect to a C&C server. It is totally harmless, and only prints commands sent by C&C. I have found two branch of this malware, and client is compatible with both of them. I found a C&C which seems to have new commands, but this client is compatible.

 * jiemi.py : This program implements the 'obfuscation' used by the malware in order to hide C&C domain in the binary.
