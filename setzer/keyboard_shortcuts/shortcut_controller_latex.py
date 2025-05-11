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

import os
import importlib.util
import logging
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio

from setzer.app.service_locator import ServiceLocator
from setzer.keyboard_shortcuts.shortcut_controller import ShortcutController
from setzer.popovers.popover_manager import PopoverManager


def load_custom_shortcuts_module(filename='~/.config/setzer/custom_shortcuts.py'):
    """
    Dynamically load a Python module defining custom shortcut mappings.

    The module should define:
      insert_before_after = [
          (['\\textbf{', '}'], ['<Control>b']),
          (['\\textit{', '}'], ['<Control>i']),
          ...
      ]
      insert_symbol = [
          (['\\frac{•}{•}'], ['<Alt><Shift>f']),
          ...
      ]
    """
    path = os.path.expanduser(filename)
    if not os.path.isfile(path):
        logging.info(f"Custom shortcuts file not found: {path}")
        return None
    spec = importlib.util.spec_from_file_location('custom_shortcuts', path)
    if not spec or not spec.loader:
        logging.error(f"Failed to create spec for {path}")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        logging.error(f"Error loading custom shortcuts module: {e}")
        return None
    return module

class ShortcutControllerLaTeX(ShortcutController):

    def __init__(self):
        super().__init__()

        setup = logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.main_window = ServiceLocator.get_main_window()
        self.workspace = ServiceLocator.get_workspace()
        self.actions = self.workspace.actions

        self.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)

        # fixed shortcuts
        self.create_and_add_shortcut('<Control>k', self.actions.toggle_comment)
        self.create_and_add_shortcut('<Control>quotedbl', self.shortcut_quotes)

        # now load custom overrides for just those outsourceable mappings
        custom = load_custom_shortcuts_module()
        if custom:
            # override insert_before_after mappings
            for param, accels in getattr(custom, 'insert_before_after', []):
                self.set_accels_for_insert_before_after_action(param, accels)
                logging.info(f"Custom B/A shortcut: {param} -> {accels}")
            # override insert_symbol mappings
            for param, accels in getattr(custom, 'insert_symbol', []):
                self.set_accels_for_insert_symbol_action(param, accels)
                logging.info(f"Custom symbol shortcut: {param} -> {accels}")

    def set_accels_for_insert_before_after_action(self, parameter, accels):
        self.main_window.app.set_accels_for_action(
            Gio.Action.print_detailed_name('win.insert-before-after', GLib.Variant('as', parameter)),
            accels
        )

    def set_accels_for_insert_symbol_action(self, parameter, accels):
        self.main_window.app.set_accels_for_action(
            Gio.Action.print_detailed_name('win.insert-symbol', GLib.Variant('as', parameter)),
            accels
        )

    def shortcut_quotes(self, accel_group=None, window=None, key=None, mask=None):
        PopoverManager.popup_at_button('quotes_menu')

