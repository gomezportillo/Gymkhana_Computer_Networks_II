#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux.printing_format import green_nd_bold, end_format
from aux.my_variables import uclm_url, uclm_port1
from steps.step import Step

class Step0(Step):

    def __init(self):
        super().__init__()

    def run(self):

        print ("{}{}{}".format(green_nd_bold,
                               "\n#### STEP 0: BASIC TCP CONNECTION\n",
                               end_format))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet, tcp
        sock.connect( (uclm_url, uclm_port1) )
        step1_instructions, client = sock.recvfrom(1024)
        sock.close()

        #print(step1_instructions.decode())
        code_step1 = step1_instructions[:5].decode()

        print ("Code received from the UCLM server: {0}".format(code_step1))

        return code_step1
