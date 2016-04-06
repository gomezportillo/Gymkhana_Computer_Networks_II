#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys

try:
    from gi.repository import Gtk as gtk
except:
    print("GTK Not Available")
    sys.exit(1)

from gymkhana.steps import step0, step1, step2, step3, step4, step5

class GUI:
    builder = None
    window = None

    def __init__(self):

        self.builder = gtk.Builder()
        self.builder.add_from_file('glade/gymkhana.glade')

        handlers = {
            "solve_gymkhana_button_clicked": self.solve_gymkhana,
            "menu_quit": self.exit,
            "menu_about": self.show_about,
        }

        self.step0 = step0.Step0()
        self.step1 = step1.Step1()
        self.step2 = step2.Step2()
        self.step3 = step3.Step3()
        self.step4 = step4.Step4()
        self.step5 = step5.Step5()

        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("main_window")
        self.window.connect('destroy', gtk.main_quit)
        self.window.show()

    def solve_gymkhana(self, button): #solve gymkhana's button listener

        self.reset_progressbar()

        try:
            self.update_message("Solving step 0...", )
            code_step1 = self.step0.run()

            self.update_message("Solving step 1...")
            code_step2 = self.step1.run(code_step1)

            self.update_message("Solving step 2...")
            code_step3 = self.step2.run(code_step2)

            self.update_message("Solving step 3...")
            code_step4 = self.step3.run(code_step3)

            self.update_message("Solving step 4...")
            code_step5 = self.step4.run(code_step4)

            self.update_message("Solving step 5...")
            self.step5.run(code_step5)

            self.update_message("Gymkhana completed!")
        except KeyboardInterrupt:
            raise

    def update_message(self, message="Llevamos un", step=0.142):
        progress_bar = self.builder.get_object('progress_bar')
        fraction = round(progress_bar.get_fraction() + step, 3)
        progress_bar.set_fraction(fraction)
        progress_bar.set_text('{} {}%'.format(message, int(fraction*100)))

    def reset_progressbar(self):
        progress_bar = self.builder.get_object('progress_bar')
        progress_bar.set_fraction(0)
        progress_bar.set_text('0%')

    def show_about(self, button):
        gtk_window_set_modal()
        self.dialog = gtk.AboutDialog()
        self.dialog.set_name("Gymkhana solver")
        self.dialog.set_authors(['\nPedro-Manuel Gomez-Portillo Lopez'])
        license_file = open(os.path.join('data', 'license', 'LICENSE.txt'), 'r')
        self.dialog.set_license(license_file.read())
        self.dialog.run()
        self.dialog.destroy()

    def exit(self, button):
        sys.exit(0)

gui = GUI()
gtk.main()
