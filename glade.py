#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys

try:
    from gi.repository import Gtk as gtk
except:
    print("GTK Not Available")
    sys.exit(1)

from gymkhana.gymkana_solver import GymkhanaSolver

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

        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("main_window")
        self.window.connect('destroy', gtk.main_quit)
        self.window.show()

    def solve_gymkhana(self, button): #solve gymkhana's button listener

        solve_button = self.builder.get_object('solve_gymkhana_button')
        solve_button.set_sensitive(False)

        self.reset_progressbar()

        gs = GymkhanaSolver(self)
        gs.solve_gymkhana()

        solve_button.set_sensitive(True)

    def update_progressbar_message(self, message="Llevamos un ", step=0.143):
        progress_bar = self.builder.get_object('progress_bar')
        fraction = round(progress_bar.get_fraction() + step, 3)
        progress_bar.set_fraction(fraction)
        progress_bar.set_text('{} {}%'.format(message, int(fraction*100)))

        while gtk.events_pending(): #force to update the progress bar
            gtk.main_iteration_do(True)

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
