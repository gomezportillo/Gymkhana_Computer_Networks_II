#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os

try:
    from gi.repository import Gtk as gtk
except:
    print("GTK Not Available")
    sys.exit(1)

class GUI:
    builder = None
    window = None

    def __init__(self):

        self.builder = gtk.Builder()
        self.builder.add_from_file('glade/gymkhana.glade')

        handlers = {
            "solve_gymkhana_button_clicked": self.solve_gymkhana,
            "menu_quit_": self.exit,
            "menu_about": self.show_about,
        }

        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("main_window")
        self.window.connect('destroy', gtk.main_quit)
        self.window.show()

    def solve_gymkhana(self, button):
        pass


    def show_about(self, button):
        self.dialog = gtk.AboutDialog()
        self.dialog.set_name("Gymkhana solver")
        self.dialog.set_authors(['\nPedro-Manuel Gomez-Portillo Lopez'])
        license_file = open(os.path.join('data', 'license', 'LICENSE.txt'), 'r')
        self.dialog.set_license(license_file.read())
        self.dialog.run()
        self.dialog.destroy()

    def exit(self, button):
        sys.exit(1)

gui = GUI()
gtk.main()
