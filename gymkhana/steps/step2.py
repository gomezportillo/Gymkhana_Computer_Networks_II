#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import sys

from gymkhana.aux.printing_format import green_nd_bold, red_nd_bold, end_format
from gymkhana.aux.my_variables import uclm_url
from gymkhana.steps.step import Step

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

            operation = ""
            balanced = False

            #always when using TCP it must be checked whether the full message has been received
            while not balanced:
                partial_operation, client = sock.recvfrom(1024)
                operation += partial_operation.decode()
                balanced = self.count_parenthesis(operation)

            if operation[0] is not '(':
                #print(operation.decode())
                return operation[:5]

            result = self.compute_operation(operation)
            sock.send(result.encode())

        sock.close()

    def count_parenthesis(self, operation):

        dispared_parenthesis = 0

        for char in operation:
            if char is '(':
                dispared_parenthesis += 1
            else:
                if char is ')':
                    dispared_parenthesis -= 1

        return dispared_parenthesis is 0

    def compute_operation(self, operation):

        print("Original\t{}".format(operation))

        str_len = len(operation)
        i = 0

        while i < str_len:
            if operation[i] == '/':
                operation = "{}/{}".format(operation[:i], operation[i:])
                str_len += 1
                i += 1

            i += 1

        try:
            result = "{}".format(eval(operation))

        except SyntaxError as err:
            print("{}{}{}".format(red_nd_bold,
                                  "Error receiving operations. Aborting program.\n",
                                  end_format))
            sys.exit(1)

        print("Worked out\t{}\tResult\t{}".format(operation, result))

        return "({})".format(result)
