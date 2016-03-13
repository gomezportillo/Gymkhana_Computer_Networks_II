#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux import printing_format as p_f
from aux import my_variables as m_v

class Step0():

    def __init(self):
        pass

    def run(self):

        print(p_f.blue_nd_bold + "Pedro Manuel Gómez-Portillo López, 2ºA" + p_f.end_format)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet, tcp

        sock.connect((uclm_url, uclm_port1))
        msg, client = sock.recvfrom(1024)

        #print("\n\n" + msg.decode())  		#printing the 1 step instrucctions

        sock.close()

        return msg[:5].decode()
