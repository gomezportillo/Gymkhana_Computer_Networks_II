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

from gymkhana.steps import step0, step1, step2, step3, step4, step5

from gymkhana.aux.printing_format import green_nd_bold, blue_nd_bold, end_format

import sys

class GymkhanaSolver:

    def __init__(self, gui):
        if len(sys.argv) != 1:
            print(__doc__.format(__file__))
            sys.exit(1)

        self.gui = gui

        print("{}{}{}{}{}".format(green_nd_bold, "\n#### PYTHON GYMKHANA\n",
                                  blue_nd_bold, "\nPedro Manuel Gómez-Portillo López, 2ºA",
                                  end_format))

    def solve_gymkhana(self):



        try:
            code_step1 = self.step0.run()
            self.gui.update_message("Resolviendo etapa 1...")
            code_step2 = self.step1.run(code_step1)

            code_step3 = self.step2.run(code_step2)

            code_step4 = self.step3.run(code_step3)

            code_step5 = self.step4.run(code_step4)

            self.step5.run(code_step5)

        except KeyboardInterrupt:
            raise
