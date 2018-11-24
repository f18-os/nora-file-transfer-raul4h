#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
import params
from framedSock import FramedStreamSock
from threading import Thread, Lock
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


inputFile = input("Please enter file name: ")

if(not os.path.isfile(inputFile)):
    print("No such file exist")
    exit()

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

lock = Lock()

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               #print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               #print(" error: %s" % msg)
               s = None
               continue
           try:
               #print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               #print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)

       lock.acquire()

       print("Sending " + inputFile)
       fs.sendmsg(inputFile.encode())
       payload = fs.receivemsg()
       if(payload.decode() == "Ready"):
           sentFile = open(inputFile, "r")
           data = sentFile.read(100)
           while(data):
               fs.sendmsg(data.encode())
               time.sleep(0.001)
               data = sentFile.read(100)
           fs.sendmsg(b"exit")
       lock.release()



       # print("sending hello world")
       # fs.sendmsg(b"hello world")
       # print("received:", fs.receivemsg())

       # fs.sendmsg(b"hello world")
       # print("received:", fs.receivemsg())

for i in range(10):
    ClientThread(serverHost, serverPort, debug)
