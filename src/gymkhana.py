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
import time
import urllib.request
import urllib.error
import struct

if len(sys.argv) != 1:
    print(__doc__.format(__file__))
    sys.exit(1)

print("{}{}{}{}{}".format(p_f.green_nd_bold, "#### PYTHON GYMKHANA\n",
                          p_f.blue_nd_bold, "Pedro Manuel Gómez-Portillo López, 2ºA",
                          p_f.end_format))

step0 = step0.Step0()
step1 = step0.Step1()
step2 = step0.Step2()
step3 = step0.Step3()
step4 = step0.Step4()
step5 = step0.step5()

try:
    server_code = step0.run()

    step1.run(server_code)

    step3_instructions = step2.run()

    downloaded_file = step3.run(step3_instructions)

    http_instructions = step4.run(downloaded_file)

    step5.run(http_instructions)

except KeyboardInterrupt:
    pass
