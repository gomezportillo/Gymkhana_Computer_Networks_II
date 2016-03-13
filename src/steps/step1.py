#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import threading

from aux import printing_format as p_f
from aux import my_variables as m_v

mutex = threading.Event()   #mutex semaphore for thread syncronizing

class Step1(Step):

    def __init__(self):
        super().__init__()

    def run(self, server_code):
        print("{0}{1}{2}".format(p_f.green_nd_bold,
                                "#### STEP 1: UDP THREADING SERVER\n",
                                p_f.end_format))

        t=threading.Thread(target=myUDPserver)
        t.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, udp
        my_msg_str = server_code+" "+str(my_UDPserver_port)
        print("My message to the UCML server: {0}\n".format(my_msg_str))
        sock.sendto(my_msg_str.encode(), (uclm_url, uclm_port1))

        sock.close()

def myUDPserver(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, udp
    sock.settimeout(4)
    sock.bind(('', my_UDPserver_port))
    msg, client = sock.recvfrom(2048)

    #print("\n\n"+msg.decode())			#printng the 2 step instruccionts

    global uclm_port2
    uclm_port2 = msg[:4].decode()

    sock.close()
    mutex.set()   #announcing you already have the message
