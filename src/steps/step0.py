#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux import printing_format as p_f
from aux import my_variables as m_v

class Step0(Step):

    def __init(self):
        super().__init__()

    def run(self):

        print("{0}{1}{2}".format(p_f.green_nd_bold,
                                "#### STEP 0: BASIC TCP CONNECTION\n",
                                p_f.end_format))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet, tcp
        sock.connect((m_v.uclm_url, m_v.uclm_port1))
        msg, client = sock.recvfrom(1024)
        sock.close()

        #print("\n\n" + msg.decode())  		#printing the 1 step instrucctions
        code = msg[:5].decode()

        prin("Code recived from the UCLM server: {0}".format(code))

        return code
