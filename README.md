# afterburner

*An afterburner is a component present on some jet engines, mostly those used on supersonic aircraft. Its purpose is to provide an increase in thrust, usually for supersonic flight, takeoff and for combat situations. Afterburning is achieved by injecting additional fuel into the jet pipe downstream of the turbine. The advantage of afterburning is significantly increased thrust.*

## Background
Botnets are everywhere. Some are used to spread malware, others to control
devices, and some are used to launch powerful denial of services by flooding 
targets.

The Botmaster send orders to its bot through a Command and Control (C&C) 
server. All bots connect to the C&C. In ancient times, the C&C was usually
an IRC channel [reference needed]. Today, it's more custom protocols.

## Ideas
C&C servers are very ephemeral. Botmaster can change them at anytime. Clients
can be recompiled, modified, so they are not very stable in time. I think that
the network protocol is the one that doesn't change really often.

So, the idea is to write innocuous client implementing the network protocol
used by a botnet, and monitor its activity.

## Wake-Up project
A malware has been reversed here http://0x90909090.blogspot.fr/2017/08/meet-wake-malware-ddos-and-more.html
You can find in WakeUp directory a client and some utilities.
