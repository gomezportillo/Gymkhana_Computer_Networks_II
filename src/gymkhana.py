#!/usr/bin/python3
# -*- coding:utf-8 -*-

"Usage: sudo python3 {0}"

#***********************************************************************
# Author: Pedro-Manuel Gómez-Portillo López    pedroma.almagro@gmail.com
#
# You can redistribute and/or modify this file under the terms of the
# GNU General Public License ad published by the Free Software
# Foundation, either version 3 of the License, or (at your option)
# and later version. See <http://www.gnu.org/licenses/>.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# *********************************************************************/

from steps import step0, step1, step2, step3, step4, step5

from aux import my_variables as m_v
from aux import printing_format as p_f

import sys
import socket
import threading
import time
import urllib.request
import urllib.error
import struct

mutex = threading.Event()                       #mutex semaphore for thread syncronizing

print(p_f.green_nd_bold + "----------------------PYTHON GYMKHANA------------------------------------------------\n" + p_f.end_format)

##########################################################################################
#STEP 1-----------------------------------------------------------------------------------
##########################################################################################
def step1(server_code):
    print(p_f.green_nd_bold + "----------------------STEP 1: UDP THREADING SERVER-----------------------------------\n" + p_f.end_format)

    t=threading.Thread(target=myUDPserver)
    t.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udp
    my_msg_str = server_code+" "+str(my_UDPserver_port)
    print("My message to the UCML server: "+my_msg_str +"\n")
    sock.sendto(my_msg_str.encode(), (uclm_url, uclm_port1))

    sock.close()


def myUDPserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udp
    sock.settimeout(4)
    sock.bind(('', my_UDPserver_port))
    msg, client = sock.recvfrom(2048)

    #print("\n\n"+msg.decode())			#printng the 2 step instruccionts

    global uclm_port2
    uclm_port2 = msg[:4].decode()

    sock.close()
    mutex.set()   #announcing you already have the message



##########################################################################################
#STEP 2-----------------------------------------------------------------------------------
##########################################################################################
def step2():
    print(green_nd_bold + "----------------------STEP 2: RECEIVING AND COMPUTING OPERATIONS THROUGH TCP---------\n" + end_format)

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

def count_parenthesis(op):
    dispared_parenth = i = 0
    str_len = len(op)

    while i<str_len:
        if op[i] == '(':
            dispared_parenth+=1
        else:
            if op[i] == ')':
                dispared_parenth-=1
        i+=1

    if dispared_parenth == 0:
        return True
    else:
        return False

def compute_operation(op):
    print("Original----->"+op)

    str_len = len(op)
    i = 0
    while i<str_len:
      if op[i] == '/':
        op = op[:i] + "/" + op[i:]
        str_len+=1
        i+=1

      i+=1

    try:
        result = str(eval(op))
    except SyntaxError as err:
        print(red_nd_bold + "Error recieving operations. Aborting program.\n" + end_format)
        sys.exit()

    print("Worked out--->"+op+"\t\tResult: "+result)
    return "("+result+")"



##########################################################################################
#STEP 3-----------------------------------------------------------------------------------
##########################################################################################
def step3(instructions):
    print(green_nd_bold + "\n----------------------STEP 3: DOWNLOADING FILES THOUGH HTTP---------------------------\n" + end_format)

    #print(instructions)
    url = uclm_url2 + str(instructions[:5])
    print("Downloading file from " + url + "\n")

    try:
        my_file = urllib.request.urlopen(urllib.request.Request(url))

        downloaded_file = my_file.read().decode()

        return downloaded_file

    except URLError as err:
        print(red_nd_bold + "URL error. Exiting.\n" + end_format)
        sys.exit()
    except HTTPError as err:
        print(red_nd_bold + "HTTP error. Exiting.\n" + end_format)
        sys.exit()



##########################################################################################
#STEP 4-----------------------------------------------------------------------------------
##########################################################################################
def step4(downloaded_file):

    print(green_nd_bold + "----------------------STEP 4: ICMP ECHO REQUEST---------------------------------------\n" + end_format)

    #print(downloaded_file)

    ping_port = downloaded_file[:5]

    icmp_packet = create_icmp_packet(ping_port)

    try:
      raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    except:
      print(red_nd_bold + colorfill + "You must execute the program as root user for using RAW shockets. Exiting...\n" + end_format)
      sys.exit(1)

    raw_socket.sendto(icmp_packet, (uclm_url, 0))

    #one of both will be the default ping acknowledge answered by the machine; the other one will be the response of the server
    print("Sending ping...\n")
    rec_packet, addr = raw_socket.recvfrom(2048)
    rec_packet2, addr = raw_socket.recvfrom(2048)
    print("Receiving ping...\n")

    raw_socket.close()

    if len(rec_packet) > len(rec_packet2):
      return rec_packet[36:].decode()
    else:
      return rec_packet2[36:].decode()


#Bibliography: https://gist.github.com/pklaus/856268
def create_icmp_packet(port):
    # 1B-type 1B-code 2B-checksum 2B-identifier(random) 2B-sec number #ping packet structure
    #icmp_header = b'\x08\x00\x00\x00\x00\x00\x00\x00' #wireshark capture

    tmp_header = struct.pack('!bbHHh', 8, 0, 0, 0, 0)
    timestamp = "%x" % int(time.time())
    icmp_data = str.encode(timestamp) + str.encode(port)
    tmp_packet = tmp_header + icmp_data

    my_checksum = compute_checksum(tmp_packet)

    icmp_header = struct.pack('!bbHHh', 8, 0, my_checksum, 0, 0)
    icmp_packet = icmp_header + icmp_data


    test_checksum = compute_checksum(icmp_packet)
    if test_checksum != 0:
      print(red_nd_bold + colorfill + "Error calculating the checksum. Final checksum: " + str(test_checksum) + " (should be 0). Exiting program..." + end_format)
      sys.exit()

    return icmp_packet


#Bibliography: https://bitbucket.org/arco_group/python-net/src/tip/raw/icmp_checksum.py
def compute_checksum(data):
    retval = sum16(data)                       # sum
    retval = sum16(struct.pack('!L', retval))  # one's complement sum
    retval = (retval & 0xFFFF) ^ 0xFFFF        # one's complement
    return retval

def sum16(data):         #sum all the the 16-bit words in data
    if len(data) % 2:
        data += str.encode('\0')
    return sum(struct.unpack("!%sH" % (len(data) // 2), data))



##########################################################################################
#STEP 5-----------------------------------------------------------------------------------
##########################################################################################
def step5(instructions):
    print(green_nd_bold + "----------------------STEP 5: HTTP WEB PROXY-------------------------------------------\n" + end_format)

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

    print(yellow_nd_bold + colorfill + msg.decode() + end_format)

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

    data2 = data.split()
    url = data2[1]

    my_file = urllib.request.urlopen(urllib.request.Request(url.decode()))
    print("Downloading file "+ url.decode())
    downloaded_file = my_file.read().decode()

    clientsock.send(downloaded_file.encode())

    print("Sending file " + url.decode())

    clientsock.close()



##########################################################################################
#MAIN METHOD------------------------------------------------------------------------------
##########################################################################################
if len(sys.argv) != 1:
    print(__doc__.format(__file__))
    sys.exit(1)

try:

    step0 = step0.Step0()

    server_code = step0.run()

    step1(server_code)

    step3_instructions = step2()

    downloaded_file = step3(step3_instructions)

    http_instructions = step4(downloaded_file)

    step5(http_instructions)
except KeyboardInterrupt:
    pass
