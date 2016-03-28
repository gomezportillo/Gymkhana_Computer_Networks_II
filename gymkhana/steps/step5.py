#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import threading

from aux.printing_format import green_nd_bold, yellow_nd_bold, colorfill, end_format
from aux.my_variables import uclm_url, uclm_port3, my_TCPserver_port
from steps.step import Step

class Step5(Step):

    def __init__(self):
        super().__init__()

    def run(self, proxy_code):

        print("{}{}{}".format(green_nd_bold,
                            "#### STEP 5: HTTP WEB PROXY\n",
                            end_format))

        socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #internet, tcp
        socketserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reusable port
        socketserver.bind(('', my_TCPserver_port))
        socketserver.listen(30)
        t = threading.Thread(target = myTCPserver, args = (socketserver,))
        t.setDaemon(True)
        t.start()

        sockPROXY = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet, tcp
        sockPROXY.connect( (uclm_url, uclm_port3) )
        message = "{} {}".format(proxy_code,
                                 my_TCPserver_port)
        sockPROXY.send(message.encode())

        msg, client = sockPROXY.recvfrom(1024)

        print("{}{}{}{}".format(yellow_nd_bold,
                                colorfill,
                                msg.decode(),
                                end_format))

        socketserver.close()
        sockPROXY.close()


def myTCPserver(socketserver):

    while True:
      clientsocket, client = socketserver.accept()
      t=threading.Thread(target=download_and_send_webpage, args=(clientsocket, ))
      t.start()


def download_and_send_webpage(clientsock):

    data = clientsock.recv(1024)
    print(data.decode())

    url = data.split()[1].decode()

    print("Downloading file {}".format(url))
    url_request = Request(url)
    my_file = urlopen(url_request)
    downloaded_file = my_file.read()

    print("Sending file {}".format(url))
    clientsock.send(downloaded_file)

    clientsock.close()
