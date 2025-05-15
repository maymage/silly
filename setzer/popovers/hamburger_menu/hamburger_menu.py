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
from gi.repository import Gtk, Gdk

from setzer.dialogs.dialog_locator import DialogLocator
from setzer.popovers.helpers.popover_menu_builder import MenuBuilder
from setzer.popovers.hamburger_menu.hamburger_menu_viewgtk import HamburgerMenuView


class HamburgerMenu(object):

    def __init__(self, popover_manager, workspace):
        self.popover_manager = popover_manager
        self.workspace = workspace
        self.view = HamburgerMenuView(popover_manager)

        self.session_file_buttons = list()
        self.view.button_restore_session.connect('clicked', self.on_restore_session_click, None)

        # Update zoom level when popover shows, when document changes, or when preview changes
        self.popover_manager.connect('shown', self.update_zoom_level)
        self.workspace.connect('document_changed', self.update_zoom_level)
        self.workspace.connect('preview_state_change', self.update_zoom_level)
        
        # Update zoom when active document changes
        self.workspace.connect('active_document_changed', self.update_zoom_level)
    
        self.key_controller = Gtk.EventControllerKey()
        self.key_controller.connect('key-pressed', self.on_keypress)
        self.view.add_controller(self.key_controller)
    
    def update_zoom_level(self, *args):
        """Update the PDF preview zoom level display in the hamburger menu"""
        document = self.workspace.get_active_document()
        if document and hasattr(document, 'preview') and document.preview.pdf_filename:
            # Get the zoom level from the preview zoom manager and format as integer percentage
            zoom_level = int(document.preview.zoom_manager.zoom_level * 100)
            
            # Update the correct label - check if we're using button or child label
            zoom_label = self.view.zoom_level_button.get_child()
            if zoom_label is not None:
                zoom_label.set_text(f"{zoom_level}%")
            else:
                self.view.zoom_level_button.set_label(f"{zoom_level}%")
            
            # Enable the zoom controls
            self.view.zoom_button_box.set_sensitive(True)
        else:
            # Disable the zoom controls if no PDF preview is available
            zoom_label = self.view.zoom_level_button.get_child()
            if zoom_label is not None:
                zoom_label.set_text("—")
            else:
                self.view.zoom_level_button.set_label("—")
            
            self.view.zoom_button_box.set_sensitive(False)

    def on_keypress(self, controller, keyval, keycode, state):
        modifiers = Gtk.accelerator_get_default_mod_mask()

        if keyval == Gdk.keyval_from_name('F10'):
            if state & modifiers == 0:
                self.popover_manager.popdown()
                return True

        return False

    def on_update_recently_opened_session_files(self, workspace, recently_opened_session_files):
        items = list()
        data = recently_opened_session_files.values()
        for item in sorted(data, key=lambda val: -val['date']):
            items.append(item['filename'])
        for button in self.session_file_buttons:
            self.view.prev_sessions_box.remove(button)
        self.session_file_buttons = list()
        self.view.session_box_separator.set_visible(len(items) > 0)
        for item in items:
            button = MenuBuilder.create_button(item)
            button.connect('clicked', self.on_restore_session_click, item)
            self.view.prev_sessions_box.append(button)
            self.session_file_buttons.append(button)

    def on_restore_session_click(self, button, parameter):
        self.popover_manager.popdown()

        if parameter == None:
            DialogLocator.get_dialog('open_session').run(self.restore_session_cb)
        else:
            self.restore_session_cb(parameter)

    def restore_session_cb(self, filename):
        if filename == None: return

        unsaved_documents = self.workspace.get_unsaved_documents()
        if len(unsaved_documents) > 0:
            self.workspace.set_active_document(unsaved_documents[0])
            dialog = DialogLocator.get_dialog('close_confirmation')
            dialog.run({'unsaved_document': unsaved_documents[0], 'session_filename': filename}, self.close_confirmation_cb)
        else:
            documents = self.workspace.get_all_documents()
            for document in documents:
                self.workspace.remove_document(document)
            self.workspace.load_documents_from_session_file(filename)

    def close_confirmation_cb(self, parameters):
        document = parameters['unsaved_document']

        if parameters['response'] == 0:
            self.workspace.remove_document(document)
            self.restore_session_cb(parameters['session_filename'])
        elif parameters['response'] == 2:
            if document.get_filename() == None:
                DialogLocator.get_dialog('save_document').run(document, self.restore_session_cb, parameters['session_filename'])
            else:
                document.save_to_disk()
                self.restore_session_cb(parameters['session_filename'])
def update_zoom_level(self):
    zoom_level = self.document.preview.zoom_manager.get_zoom_level()

    if zoom_level != None:
        # Format as integer percentage instead of decimal
        self.view.zoom_level_label.set_text('{0}%'.format(int(zoom_level * 100)))