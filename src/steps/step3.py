#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

from aux import printing_format as p_f
from aux import my_variables as m_v

class Step3():

    def __init__(self):
        pass

    def run(self, instructions):

        print("{0}{1}{2}".format(green_nd_bold,
                                "\n#### STEP 3: DOWNLOADING FILES THOUGH HTTP\n",
                                end_format)

        #print(instructions)
        url = uclm_url2 + str(instructions[:5])
        print("Downloading file from {0}\n".format(url))

        try:
            my_file = urllib.request.urlopen(urllib.request.Request(url))

            downloaded_file = my_file.read()

            return downloaded_file.decode()

        except (URLError, HTTPError) as err:
            print("{}{}{}".format(red_nd_bold,
                                 err.__str__(),
                                 end_format)
            sys.exit()
