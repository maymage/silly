#!/usr/bin/env python3
# coding: utf-8

# Copyright (C) 2017-present Robert Griesel
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from setzer.dialogs.helpers.dialog_viewgtk import DialogView


class Preferences(DialogView):

    def __init__(self, main_window):
        DialogView.__init__(self, main_window)

        self.set_can_focus(False)
        self.set_size_request(400, 250)
        self.set_default_size(400, 250)
        
        # Create title label
        self.title_label = Gtk.Label.new(_('Preferences'))
        self.headerbar.set_title_widget(self.title_label)
        
        # Create a container for the view stack
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_vexpand(True)
        self.topbox.append(self.content_box)

    def set_header_widget(self, widget):
        """Set the widget that should appear in the headerbar"""
        # Remove the title label first
        self.headerbar.set_title_widget(None)
        # Set the view switcher as the title widget
        self.headerbar.set_title_widget(widget)
        
    def set_content(self, widget):
        """Set the main content widget"""
        # Remove any existing content first
        for child in self.content_box:
            self.content_box.remove(child)
        # Add the new widget
        self.content_box.append(widget)