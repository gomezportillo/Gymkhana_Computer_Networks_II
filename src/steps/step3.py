#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import sys

from aux.printing_format import green_nd_bold, end_format
from aux.my_variables import uclm_url2
from steps.step import Step

class Step3(Step):

    def __init__(self):
        super().__init__()

    def run(self, code_step3):

        print("{}{}{}".format(green_nd_bold,
                              "\n#### STEP 3: DOWNLOADING FILES THOUGH HTTP\n",
                              end_format))

        url = "{}{}".format(uclm_url2, code_step3)
        print("Downloading file from {0}\n".format(url))

        try:
            url_request = Request(url)

            downloaded_file = urlopen(url_request)

            step4_instructions = downloaded_file.read().decode()

            #print(step4_instructions)

            code_step4 = step4_instructions[:5]

            return code_step4

        except (URLError, HTTPError) as err:
            print("{}{}{}".format(red_nd_bold,
                                  err.__str__(),
                                  end_format))
            sys.exit(1)
