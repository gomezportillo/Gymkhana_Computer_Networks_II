#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux import printing_format as p_f
from aux import my_variables as m_v

class Step5(Step):

    def __init__(self):
        super().__init__()

    def run(self, instructions):
        print("{}{}{}".format(green_nd_bold,
                            "#### STEP 5: HTTP WEB PROXY\n",
                            end_format))

        #print(instructions)

        proxy_code = instructions[:5]

        socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #tcp
        socketserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reusable port
        socketserver.bind(('', my_TCPserver_port))
        socketserver.listen(30)
        t=threading.Thread(target=myTCPserver, args=(socketserver,))
        t.setDaemon(True)
        t.start()

        sockPROXY = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp
        sockPROXY.connect((uclm_url, uclm_port3))
        sockPROXY.send((str(proxy_code) + " " + str(my_TCPserver_port)).encode())

        msg, client = sockPROXY.recvfrom(1024)

        print("{}{}{}{}".format(yellow_nd_bold,
                                colorfill,
                                msg.decode(),
                                end_format)

        socketserver.close()
        sockPROXY.close()

    #ERROR: WrongResource '[Errno 104] Connection reset by peer':  is the TCP/IP equivalent of slamming the phone back on the hook.
    def myTCPserver(socketserver):
        while 1:
          clientsock, client = socketserver.accept()
          t=threading.Thread(target=download_and_send_webpage, args=(clientsock,))
          t.start()

    def download_and_send_webpage(clientsock):

        data = clientsock.recv(1024)
        print(data.decode())

        url = data.split()[1].decode()

        print("Downloading file {}".format(url))
        my_file = urllib.request.urlopen(urllib.request.Request(url))
        downloaded_file = my_file.read()

        print("Sending file {}".format(url))
        clientsock.send(downloaded_file)

        clientsock.close()
