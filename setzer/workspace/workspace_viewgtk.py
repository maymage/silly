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
from gi.repository import Adw, Gdk, Gtk, Gio

import setzer.workspace.build_log.build_log_viewgtk as build_log_view
import setzer.workspace.headerbar.headerbar_viewgtk as headerbar_view
import setzer.workspace.shortcutsbar.shortcutsbar_viewgtk as shortcutsbar_view
import setzer.workspace.preview_panel.preview_panel_viewgtk as preview_panel_view
import setzer.workspace.help_panel.help_panel_viewgtk as help_panel_view
import setzer.workspace.sidebar.sidebar_viewgtk as sidebar_view
import setzer.workspace.welcome_screen.welcome_screen_viewgtk as welcome_screen_view
import setzer.widgets.animated_paned.animated_paned as animated_paned
from setzer.app.service_locator import ServiceLocator

import os.path


class MainWindow(Adw.ApplicationWindow):

    def __init__(self, app):
        Adw.ApplicationWindow.__init__(self, application=app)

        self.app = app
        self.set_size_request(-1, 550)

        self.popoverlay = Gtk.Overlay()
        self.set_content(self.popoverlay)

        # Set up window actions including zoom controls
        self.setup_actions()

    def setup_actions(self):
        """Register window actions for the application"""
        # Add zoom actions for preview
        zoom_in_action = Gio.SimpleAction.new('preview-zoom-in', None)
        zoom_in_action.connect('activate', self.on_preview_zoom_in)
        self.add_action(zoom_in_action)
        
        zoom_out_action = Gio.SimpleAction.new('preview-zoom-out', None)
        zoom_out_action.connect('activate', self.on_preview_zoom_out)
        self.add_action(zoom_out_action)
        
        zoom_original_action = Gio.SimpleAction.new('preview-zoom-original', None)
        zoom_original_action.connect('activate', self.on_preview_zoom_original)
        self.add_action(zoom_original_action)

    def on_preview_zoom_in(self, action, parameter):
        """Handle zoom in action from hamburger menu"""
        workspace = ServiceLocator.get_workspace()
        document = workspace.get_active_document()
        if document and hasattr(document, 'preview') and document.preview.pdf_filename:
            document.preview.zoom_manager.zoom_in()
            workspace.add_change_code('preview_state_change')

    def on_preview_zoom_out(self, action, parameter):
        """Handle zoom out action from hamburger menu"""
        workspace = ServiceLocator.get_workspace()
        document = workspace.get_active_document()
        if document and hasattr(document, 'preview') and document.preview.pdf_filename:
            document.preview.zoom_manager.zoom_out()
            workspace.add_change_code('preview_state_change')

    def on_preview_zoom_original(self, action, parameter):
        """Handle reset zoom to 100% action from hamburger menu"""
        workspace = ServiceLocator.get_workspace()
        document = workspace.get_active_document()
        if document and hasattr(document, 'preview') and document.preview.pdf_filename:
            document.preview.zoom_manager.set_zoom_level(1.0)  # Reset to 100%
            workspace.add_change_code('preview_state_change')

    def create_widgets(self):
        self.shortcutsbar = shortcutsbar_view.Shortcutsbar()

        self.document_stack = Gtk.Notebook()
        self.document_stack.set_show_tabs(False)
        self.document_stack.set_show_border(False)
        self.document_stack.set_scrollable(True)
        self.document_stack.set_size_request(550, -1)
        self.document_stack.set_vexpand(True)

        self.document_stack_wrapper = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.document_stack_wrapper.append(self.shortcutsbar)
        self.document_stack_wrapper.append(self.document_stack)

        self.build_log = build_log_view.BuildLogView()
        self.build_log_paned = animated_paned.AnimatedVPaned(self.document_stack_wrapper, self.build_log, False)

        self.preview_panel = preview_panel_view.PreviewPanelView()

        self.help_panel = help_panel_view.HelpPanelView()

        self.sidebar = sidebar_view.Sidebar()

        self.preview_paned_overlay = Gtk.Overlay()
        self.preview_help_stack = Gtk.Stack()
        self.preview_help_stack.add_named(self.preview_panel, 'preview')
        self.preview_help_stack.add_named(self.help_panel, 'help')
        self.preview_paned = animated_paned.AnimatedHPaned(self.build_log_paned, self.preview_help_stack, False)
        self.preview_paned.set_wide_handle(True)
        self.preview_paned_overlay.set_child(self.preview_paned)

        self.sidebar_paned = animated_paned.AnimatedHPaned(self.sidebar, self.preview_paned_overlay, True)
        self.sidebar_paned.set_wide_handle(True)
        self.sidebar_paned.get_style_context().add_class('sidebar_paned')

        self.welcome_screen = welcome_screen_view.WelcomeScreenView()

        self.mode_stack = Gtk.Stack()
        self.mode_stack.add_named(self.welcome_screen, 'welcome_screen')
        self.mode_stack.add_named(self.sidebar_paned, 'documents')

        self.headerbar = headerbar_view.HeaderBar()
        self.headerbar.set_vexpand(False)
        self.headerbar.set_valign(Gtk.Align.START)

        self.main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.main_box.append(self.headerbar)
        self.main_box.append(self.mode_stack)
        self.popoverlay.set_child(self.main_box)

        self.css_provider = Gtk.CssProvider()
        resources_path = ServiceLocator.get_resources_path()
        self.css_provider.load_from_path(os.path.join(resources_path, 'style_gtk.css'))
        Gtk.StyleContext.add_provider_for_display(self.get_display(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.css_provider_font_size = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(self.get_display(), self.css_provider_font_size, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.css_provider_colors = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(self.get_display(), self.css_provider_colors, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        # Add CSS for theme selectors
        self.css_provider_theme_selectors = Gtk.CssProvider()
        self.css_provider_theme_selectors.load_from_data(b"""
            button.circular {
                border-radius: 32px;
                min-width: 64px;
                min-height: 64px;
            }
            
            button.theme-system {
                background: linear-gradient(145deg, #f6f5f4 0%, #f6f5f4 50%, #3d3846 50%, #3d3846 100%);
                border: 1px solid #d3d2d0;
            }
            
            button.theme-light {
                background-color: #f6f5f4;
                border: 1px solid #d3d2d0;
            }
            
            button.theme-dark {
                background-color: #3d3846;
                border: 1px solid #5e5c64;
            }
            
            button.theme-button {
                transition: transform 0.1s ease-in-out;
            }
            
            button.theme-button:hover {
                transform: scale(1.05);
            }
            
            button.selected {
                box-shadow: 0 0 0 3px #3584e4;
            }
            
            /* Simple button styling for zoom controls */
            .linked button {
                padding: 6px 8px;
                min-height: 32px;
            }
            
            .linked button:first-child {
                border-top-right-radius: 0;
                border-bottom-right-radius: 0;
            }
            
            .linked button:last-child {
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
            }
        """, -1)
        Gtk.StyleContext.add_provider_for_display(self.get_display(), self.css_provider_theme_selectors, Gtk.STYLE_PROVIDER_PRIORITY_USER)


