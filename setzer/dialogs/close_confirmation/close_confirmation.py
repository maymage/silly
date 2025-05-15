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
from gi.repository import Gtk, Adw, GLib


class CloseConfirmationDialog(object):
    """Dialog for confirming whether to save, discard, or cancel when closing a document with unsaved changes"""

    def __init__(self, main_window, workspace):
        self.main_window = main_window
        self.workspace = workspace
        self.parameters = None
        self.callback = None

    def run(self, parameters, callback):
        """Run the close confirmation dialog

        Parameters:
            parameters: Dictionary containing document info
            callback: Function to call after response

        Returns:
            None
        """
        if parameters['unsaved_document'] is None:
            return

        self.parameters = parameters
        self.callback = callback

        document = parameters['unsaved_document']

        # Create AlertDialog
        dialog = Adw.AlertDialog()
        dialog.set_heading(_('Save Changes?'))

        # Set message with document name
        doc_name = document.get_displayname()
        dialog.set_body(_("Open document \"{}\" contains unsaved changes. Changes which are not saved will be permanently lost.").format(
            GLib.markup_escape_text(doc_name)
        ))

        # Add response buttons
        dialog.add_response('cancel', _('_Cancel'))
        dialog.add_response('discard', _('_Discard'))
        dialog.add_response('save', _('_Save'))

        # Set button appearances
        dialog.set_response_appearance('discard', Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_response_appearance('save', Adw.ResponseAppearance.SUGGESTED)

        # Set default and close responses
        dialog.set_default_response('cancel')
        dialog.set_close_response('cancel')

        # Show dialog and connect to callback
        dialog.choose(self.main_window, None, self._on_dialog_response)

    def _on_dialog_response(self, dialog, result):
        """Handle dialog response"""
        try:
            response = dialog.choose_finish(result)

            if response == 'save':
                self.parameters['response'] = 2  # Save
            elif response == 'discard':
                self.parameters['response'] = 0  # Discard
            elif response == 'cancel':
                self.parameters['response'] = 1  # Cancel

            self.callback(self.parameters)

        except Exception as e:
            print(f"Dialog error: {e}")