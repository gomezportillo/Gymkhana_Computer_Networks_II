#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux import printing_format as p_f
from aux import my_variables as m_v
from steps import step

class Step2(step.Step):

    def __init__(self):
        super().__init__()

    def run(self):
        print("{}{}{}".format(green_nd_bold,
                            "#### STEP 2: RECEIVING AND COMPUTING OPERATIONS THROUGH TCP\n",
                            end_format))

        mutex.wait() #wait for the syncronization with myUDPserver() function
        global uclm_port2

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp
        sock.connect((uclm_url, int(uclm_port2)))

        while 1: #while the server keeps sending operations

            op = ""
            balanced = False

            while not balanced: #always when using from TCP we must check if we have received the full message somehow
                partial_op, client = sock.recvfrom(1024)
                op += partial_op.decode()
                balanced = count_parenthesis(op)

            if op[0] != '(':
                return op
                break

            result = compute_operation(op)
            sock.send(result.encode())

        sock.close()

    def count_parenthesis(self, op):
        dispared_parenthesis = 0
        i = 0
        str_len = len(op)

        while i<str_len:
            if op[i] == '(':
                dispared_parenthesis+=1
            else:
                if op[i] == ')':
                    dispared_parenthesis-=1
            i+=1

        return dispared_parenthesis == 0

    def compute_operation(self, op):

        str_len = len(op)
        i = 0

        print("{0}{1}".format("Original----->", op))

        while i<str_len:
          if op[i] == '/':
            op = op[:i] + "/" + op[i:]
            str_len+=1
            i+=1

          i+=1

        try:
            result = str(eval(op))
        except SyntaxError as err:
            print("{}{}{}".format(red_nd_bold,
                                    "Error recieving operations. Aborting program.\n",
                                    end_format))
            sys.exit(1)

        print("{}{}{}{}".format("Worked out--->", op, "\t\tResult: ", result))

        return "({})".format(result)
