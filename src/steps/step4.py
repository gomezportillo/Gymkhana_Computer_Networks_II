#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import struct
import time

from aux import printing_format as p_f
from aux import my_variables as m_v
from steps import step

class Step4(step.Step):

    def __init__(self):
        super().__init__()

    def run(self, downloaded_file):

        print("{}{}{}".format(green_nd_bold,
                                "#### STEP 4: ICMP ECHO REQUEST\n",
                                end_format))

        #print(downloaded_file)

        ping_port = downloaded_file[:5]

        icmp_packet = create_icmp_packet(ping_port)

        try:
          raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        except:
          print("{}{}{}{}".format(red_nd_bold,
                                colorfill,
                                "You must execute the program as root user for using RAW shockets. Exiting...\n",
                                end_format))
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
    def create_icmp_packet(self, port):
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
    def compute_checksum(self, data):
        retval = sum16(data)                       # sum
        retval = sum16(struct.pack('!L', retval))  # one's complement sum
        retval = (retval & 0xFFFF) ^ 0xFFFF        # one's complement
        return retval

    def sum16(self, data):         #sum all the the 16-bit words in data
        if len(data) % 2:
            data += str.encode('\0')
        return sum(struct.unpack("!%sH" % (len(data) // 2), data))
