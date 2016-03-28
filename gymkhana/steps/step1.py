#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import threading

from aux.printing_format import green_nd_bold, end_format
from aux.my_variables import uclm_url, uclm_port1, my_UDPserver_port
from steps.step import Step

mutex = threading.Event()   #mutex semaphore for thread syncronizing
uclm_port2 = 0

class Step1(Step):

    def __init__(self):
        super().__init__()

    def run(self, server_code):

        print("{}{}{}".format(green_nd_bold,
                                "\n#### STEP 1: UDP THREADING SERVER\n",
                                end_format))

        t=threading.Thread(target = myUDPserver)
        t.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, udp
        my_message = "{} {}".format(server_code,
                                    my_UDPserver_port)
        print("My message to the UCML server: {0}\n".format(my_message))
        sock.sendto(my_message.encode(), (uclm_url, uclm_port1) )
        sock.close()

        mutex.wait()    #waiting the code to be obtained

        global uclm_port2
        return uclm_port2

def myUDPserver():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, udp
    sock.settimeout(4)
    sock.bind( ('', my_UDPserver_port) )
    step2_instructions, client = sock.recvfrom(2048)
    sock.close()

    #print(step2_instructions.decode())

    global uclm_port2
    uclm_port2 = step2_instructions[:4].decode()

    mutex.set()         #announcing the code has been obtained
