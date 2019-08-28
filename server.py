# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:47:58 2019

@author: PRAVEEN
"""
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

user = input("Enter Username : ")
password = input("Enetr Password : ")
home = input("Home Directory : ")

ip = get_ip()
port=21
authorizer = DummyAuthorizer()
authorizer.add_user(user, password, home, perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

handler.banner = "FTP at " + ip + ":" + str(port) + " is ready."

server = FTPServer((ip, port), handler)
server.serve_forever()