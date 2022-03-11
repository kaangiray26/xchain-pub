#!/usr/bin/python
# -*- encoding:utf-8 -*-

import os
from xorlib import XLib
from zipfile import ZipFile

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("gtk-contained-dark.css")
Gtk.StyleContext.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class XChain:
    def __init__(self):
        self.mode = 0
        self.xlib = XLib
        self.setup()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("xchain.glade")

        self.builder.connect_signals(self)

        self.status = self.builder.get_object("statusBar")
        self.shares = self.builder.get_object("shareTotal")

        self.encryptList = self.builder.get_object("itemListEnc")
        self.decryptList = self.builder.get_object("itemListDec")
        self.lists = [self.encryptList, self.decryptList]

        self.main_window = self.builder.get_object("main_Window")
        self.main_window.show_all()

    def setup(self):
        if 'encrypted' not in os.listdir('.'):
            os.makedirs('encrypted')
        if 'decrypted' not in os.listdir('.'):
            os.makedirs('decrypted')

    def exitApp(self, *args):
        Gtk.main_quit()

    def changeMode(self, *args):
        pos = args[-1]
        self.mode = pos
        self.status.push(0, "Mode changed.")

    def add_filter(self, dialog):
        filter = Gtk.FileFilter()
        filter.set_name("XChain Keys")
        filter.add_pattern("*\.xc")
        dialog.add_filter(filter)

    def addFile(self, *args):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=None, action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        if self.mode == 1:
            self.add_filter(dialog)
        response = dialog.run()

        f_count = 0

        if response == Gtk.ResponseType.OK:
            for fname in dialog.get_filenames():
                self.lists[self.mode].append((fname,))
                f_count += 1
        dialog.destroy()

        if f_count == 1:
            self.status.push(0, f"Added {f_count} file.")
        elif f_count > 1:
            self.status.push(0, f"Added {f_count} files.")

    def clearFiles(self, *args):
        self.lists[self.mode].clear()
        self.status.push(0, "Files cleared.")

    def runOperation(self, *args):
        self.status.push(0, "Running operation...")
        if self.mode == 0:
            self.encrypt_files()
        else:
            self.decrypt_files()

    def encrypt_files(self):
        shares = self.shares.get_value_as_int()
        if not len(self.lists[0]):
            self.status.push(0, "Please add at least 1 file.")
            return

        self.status.push(0, "Creating keys...")
        if len(self.lists[0]) == 1:
            fpath = self.lists[0][0][0]
            token = self.xlib.encrypt(fpath, shares)
            self.status.push(
                0, f"Keys created, check out the 'encrypted' folder for keys starting with '{token}'")
            return

        if 'xchain.zip' in os.listdir('.'):
            os.remove('xchain.zip')
        with ZipFile('xchain.zip', 'w') as zip:
            for row in self.lists[0]:
                zip.write(filename=row[0], arcname=os.path.basename(row[0]))
        token = self.xlib.encrypt('xchain.zip', shares)
        os.remove('xchain.zip')
        self.status.push(
            0, f"Keys created, check out the 'encrypted' folder for keys starting with '{token}'")
        return

    def decrypt_files(self):
        if not len(self.lists[1]):
            self.status.push(0, "Please add at least 1 file.")
            return

        keys = [row[0] for row in self.lists[1]]
        token = self.xlib.decrypt(keys)
        self.status.push(0, f"'{token}' successfully decrypted.")


if __name__ == "__main__":
    xc = XChain()
    Gtk.main()
