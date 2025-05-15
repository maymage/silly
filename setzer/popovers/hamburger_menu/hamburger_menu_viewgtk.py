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
from gi.repository import Gtk

from setzer.popovers.helpers.popover_menu_builder import MenuBuilder
from setzer.popovers.helpers.popover import Popover

# Import Adwaita
import gi
gi.require_version('Adw', '1')
from gi.repository import Adw, Pango


class HamburgerMenuView(Popover):

    def __init__(self, popover_manager):
        Popover.__init__(self, popover_manager)

        self.set_width(280)

        self.button_save_as = MenuBuilder.create_button(_('Save Document As') + '...', shortcut=_('Shift') + '+' + _('Ctrl') + '+S')
        self.button_save_as.set_action_name('win.save-as')
        self.add_closing_button(self.button_save_as)

        self.button_save_all = MenuBuilder.create_button(_('Save All Documents'))
        self.button_save_all.set_action_name('win.save-all')
        self.add_closing_button(self.button_save_all)

        self.add_widget(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        # Theme selector with three circles directly in main menu
        self.theme_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
        self.theme_box.set_halign(Gtk.Align.CENTER)
        self.theme_box.set_margin_top(10)
        self.theme_box.set_margin_bottom(10)
        
        # System theme button
        self.system_theme_button = self.create_theme_button('system', _('System'))
        self.theme_box.append(self.system_theme_button)
        
        # Light theme button
        self.light_theme_button = self.create_theme_button('light', _('Light'))
        self.theme_box.append(self.light_theme_button)
        
        # Dark theme button
        self.dark_theme_button = self.create_theme_button('dark', _('Dark'))
        self.theme_box.append(self.dark_theme_button)
        
        self.add_widget(self.theme_box)
        
        # Simple zoom controls with zoom value between minus and plus buttons
        self.zoom_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.zoom_box.set_margin_top(10)
        self.zoom_box.set_margin_bottom(10)
        self.zoom_box.set_halign(Gtk.Align.CENTER)
        
        # Create a linked button group
        self.zoom_button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.zoom_button_box.add_css_class("linked")
        
        # Zoom out button
        self.zoom_out_button = Gtk.Button.new_from_icon_name("zoom-out-symbolic")
        self.zoom_out_button.set_action_name("win.preview-zoom-out")
        self.zoom_button_box.append(self.zoom_out_button)
        
        # Zoom level button in the center (acts as reset)
        self.zoom_level_button = Gtk.Button()
        self.zoom_level_button.set_action_name("win.preview-zoom-original")
        
        # Create label with system monospace font
        from gi.repository import Pango
        from setzer.app.font_manager import FontManager
        
        # Create label with system monospace font
        zoom_label = Gtk.Label.new("100%")
        zoom_label.set_width_chars(4)  # Set width for the label
        
        # Get system font and modify to bold
        font_desc = Pango.FontDescription.from_string(FontManager.default_font_string)
        font_desc.set_weight(Pango.Weight.BOLD)  # Make it bold
        
        # Apply the font to the label
        attr_list = Pango.AttrList()
        attr_list.insert(Pango.attr_font_desc_new(font_desc))
        zoom_label.set_attributes(attr_list)
        
        # Set the label as the button's child
        self.zoom_level_button.set_child(zoom_label)
        self.zoom_button_box.append(self.zoom_level_button)
        
        # Zoom in button
        self.zoom_in_button = Gtk.Button.new_from_icon_name("zoom-in-symbolic")
        self.zoom_in_button.set_action_name("win.preview-zoom-in")
        self.zoom_button_box.append(self.zoom_in_button)
        
        self.zoom_box.append(self.zoom_button_box)
        
        self.add_widget(self.zoom_box)
        
        self.add_widget(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))
        
        self.add_menu_button(_('Session'), 'session')

        self.add_widget(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        self.button_preferences = MenuBuilder.create_button(_('Preferences'))
        self.button_preferences.set_action_name('win.show-preferences-dialog')
        self.add_closing_button(self.button_preferences)

        self.add_widget(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        self.button_shortcuts = MenuBuilder.create_button(_('Keyboard Shortcuts'), shortcut=_('Ctrl') + '+?')
        self.button_shortcuts.set_action_name('win.show-shortcuts-dialog')
        self.add_closing_button(self.button_shortcuts)

        self.button_about = MenuBuilder.create_button(_('About'))
        self.button_about.set_action_name('win.show-about-dialog')
        self.add_closing_button(self.button_about)

        self.add_widget(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        self.button_close_all = MenuBuilder.create_button(_('Close All Documents'))
        self.button_close_all.set_action_name('win.close-all-documents')
        self.add_closing_button(self.button_close_all)

        self.button_close_active = MenuBuilder.create_button(_('Close Document'), shortcut=_('Ctrl') + '+W')
        self.button_close_active.set_action_name('win.close-active-document')
        self.add_closing_button(self.button_close_active)

        self.button_quit = MenuBuilder.create_button(_('Quit'), shortcut=_('Ctrl') + '+Q')
        self.button_quit.set_action_name('win.quit')
        self.add_closing_button(self.button_quit)

        # session submenu
        self.add_page('session', _('Session'))

        self.session_explaination = Gtk.Label.new(_('Save the list of open documents in a session file\nand restore it later, a convenient way to work\non multiple projects.'))
        self.session_explaination.set_xalign(0)
        self.session_explaination.get_style_context().add_class('explaination')
        self.session_explaination.set_margin_top(8)
        self.session_explaination.set_margin_bottom(11)

        self.button_restore_session = MenuBuilder.create_button(_('Restore Previous Session') + '...')
        self.button_save_session = MenuBuilder.create_button(_('Save Current Session') + '...')
        self.button_save_session.set_action_name('win.save-session')

        self.session_box_separator = Gtk.Separator()
        self.session_box_separator.set_visible(False)

        self.prev_sessions_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        self.add_widget(self.session_explaination, pagename='session')
        self.add_widget(self.button_restore_session, pagename='session')
        self.register_button_for_keyboard_navigation(self.button_restore_session, pagename='session')
        self.add_closing_button(self.button_save_session, pagename='session')
        self.add_widget(self.session_box_separator, pagename='session')
        self.add_widget(self.prev_sessions_box, pagename='session')
        
        # Theme submenu removed - theme buttons are now in main menu
        
    def create_theme_button(self, theme_id, label_text):
        """Create a circular theme button in GNOME style"""
        from gi.repository import Adw
        from setzer.app.service_locator import ServiceLocator
        
        # Get settings
        settings = ServiceLocator.get_settings()
        current_theme = settings.get_value('preferences', 'theme')
        
        # Create a box for the button contents
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        box.set_halign(Gtk.Align.CENTER)
        
        # Create the circular button
        button = Gtk.Button()
        button.set_size_request(40, 40)  # Make it more compact
        
        # Use GTK4 css_classes instead of get_style_context()
        button.add_css_class('circular')
        button.add_css_class(f'theme-{theme_id}')
        
        # Add selected indicator
        if current_theme == theme_id:
            button.add_css_class('selected')
        
        # Set up the button click handler
        button.connect('clicked', self.on_theme_button_clicked, theme_id)
        
        # Add hover feedback
        button.add_css_class('theme-button')
        
        # Add the button to our container
        box.append(button)
        
        # Add a label below the button
        label = Gtk.Label.new(label_text)
        label.add_css_class('caption')
        box.append(label)
        
        return box
        
    def on_theme_button_clicked(self, button, theme_id):
        from gi.repository import Adw
        from setzer.app.service_locator import ServiceLocator
        
        # Get settings and style manager
        settings = ServiceLocator.get_settings()
        style_manager = Adw.StyleManager.get_default()
        
        # Update settings
        settings.set_value('preferences', 'theme', theme_id)
        
        # Update the theme
        if theme_id == 'system':
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        elif theme_id == 'light':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif theme_id == 'dark':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            
        # Update UI to show which button is selected
        # In GTK4, we need to iterate differently through children
        child = self.theme_box.get_first_child()
        while child:
            if isinstance(child, Gtk.Box):
                button = child.get_first_child()
                if button and button.has_css_class('selected'):
                    button.remove_css_class('selected')
            child = child.get_next_sibling()
                    
        # Find the clicked button and mark it as selected
        child = self.theme_box.get_first_child()
        while child:
            if isinstance(child, Gtk.Box):
                button = child.get_first_child()
                if button and button.has_css_class(f'theme-{theme_id}'):
                    button.add_css_class('selected')
            child = child.get_next_sibling()
        
        # Keep the menu open - don't close it after theme selection

# Remove the duplicate AdwSplitButton implementation since we're using the standard buttons