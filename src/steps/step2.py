#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import sys

from aux.printing_format import green_nd_bold, red_nd_bold, end_format
from aux.my_variables import uclm_url
from steps.step import Step

class Step2(Step):

    def __init__(self):
        super().__init__()

    def run(self, uclm_port2):

        print("{}{}{}".format(green_nd_bold,
                            "#### STEP 2: RECEIVING AND COMPUTING OPERATIONS THROUGH TCP\n",
                            end_format))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet, tcp
        sock.connect( (uclm_url, int(uclm_port2)) )

        #while the server keeps sending operations
        while True:

            op = ""
            balanced = False

            #always when using from TCP we must check if we have received the full message somehow
            while not balanced:
                partial_op, client = sock.recvfrom(1024)
                op += partial_op.decode()
                balanced = self.count_parenthesis(op)

            if op[0] != '(':
                return op[:5]
                #break

            result = self.compute_operation(op)
            sock.send(result.encode())

        sock.close()

    def count_parenthesis(self, op):

        dispared_parenthesis = 0

        for i in range(0, len(op)):
            if op[i] == '(':
                dispared_parenthesis += 1
            else:
                if op[i] == ')':
                    dispared_parenthesis -= 1
            i+=1

        return dispared_parenthesis == 0

    def compute_operation(self, op):

        print("{0}{1}".format("Original\t", op))

        str_len = len(op)
        i = 0

        while i<str_len:
            if op[i] == '/':
                op = op[:i] + "/" + op[i:]
                str_len+=1
                i+=1

            i+=1

        try:
            result = "{}".format(eval(op))
        except SyntaxError as err:
            print("{}{}{}".format(red_nd_bold,
                                "Error recieving operations. Aborting program.\n",
                                end_format))
            sys.exit(1)

        print("{}{}{}{}".format("Worked out\t", op, "\tResult: ", result))

        return "({})".format(result)
