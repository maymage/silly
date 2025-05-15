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
from gi.repository import Adw, Gdk, Gtk
import os


class ColorManager():

    main_window = None
    cached_colors = {}
    debug_mode = True  # Set to True to enable theme debugging

    def init(main_window):
        ColorManager.main_window = main_window
        
        # Clear cache when theme changes
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect('notify::dark', ColorManager.on_color_scheme_changed)
        
        # Debug info
        if ColorManager.debug_mode:
            print(f"ColorManager initialized. Dark mode: {style_manager.get_dark()}")
            print(f"Color scheme: {style_manager.get_color_scheme()}")
            
        # Create custom CSS for dark theme if it doesn't automatically apply
        ColorManager.apply_custom_css()
    
    def apply_custom_css():
        """Apply custom CSS to ensure dark theme works properly"""
        style_manager = Adw.StyleManager.get_default()
        
        css_data = """
        /* Additional styles to help with dark theme */
        .main-window.dark {
            background-color: #242424;
            color: #ffffff;
        }
        
        .main-window.light {
            background-color: #ffffff;
            color: #000000;
        }
        """
        
        provider = Gtk.CssProvider()
        provider.load_from_data(css_data.encode())
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Update main window class for theme
        if ColorManager.main_window:
            if style_manager.get_dark():
                ColorManager.main_window.add_css_class("dark")
                ColorManager.main_window.remove_css_class("light")
            else:
                ColorManager.main_window.add_css_class("light")
                ColorManager.main_window.remove_css_class("dark")
    
    def on_color_scheme_changed(style_manager, pspec):
        # Clear the cache when theme changes
        ColorManager.cached_colors = {}
        
        # Debug output
        if ColorManager.debug_mode:
            print(f"Theme changed. Dark mode: {style_manager.get_dark()}")
            print(f"Color scheme: {style_manager.get_color_scheme()}")
        
        # Update CSS classes
        ColorManager.apply_custom_css()

    def get_ui_color(name):
        # Check cache first for performance
        if name in ColorManager.cached_colors:
            return ColorManager.cached_colors[name]
        
        # Get color from style context
        success, rgba = ColorManager.main_window.get_style_context().lookup_color(name)
        if success:
            ColorManager.cached_colors[name] = rgba
            return rgba
        
        # Return fallback color if lookup fails
        return ColorManager.get_fallback_color(name)
    
    def get_fallback_color(name):
        # Provide fallback colors for common color names
        is_dark = Adw.StyleManager.get_default().get_dark()
        
        if name == 'theme_fg_color':
            return Gdk.RGBA(1.0, 1.0, 1.0, 1.0) if is_dark else Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        elif name == 'theme_bg_color':
            return Gdk.RGBA(0.2, 0.2, 0.2, 1.0) if is_dark else Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
        elif name == 'theme_selected_bg_color':
            return Gdk.RGBA(0.25, 0.5, 0.9, 1.0)
        elif name == 'theme_selected_fg_color':
            return Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
        elif name == 'theme_text_color':
            return Gdk.RGBA(1.0, 1.0, 1.0, 1.0) if is_dark else Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        elif name == 'theme_base_color':
            return Gdk.RGBA(0.15, 0.15, 0.15, 1.0) if is_dark else Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
        else:
            # Default fallback color
            return Gdk.RGBA(0.5, 0.5, 0.5, 1.0)

    def get_ui_color_string(name):
        color_rgba = ColorManager.get_ui_color(name)
        color_string = '#'
        color_string += format(int(color_rgba.red * 255), '02x')
        color_string += format(int(color_rgba.green * 255), '02x')
        color_string += format(int(color_rgba.blue * 255), '02x')
        return color_string

    def get_ui_color_string_with_alpha(name):
        color_rgba = ColorManager.get_ui_color(name)
        color_string = '#'
        color_string += format(int(color_rgba.red * 255), '02x')
        color_string += format(int(color_rgba.green * 255), '02x')
        color_string += format(int(color_rgba.blue * 255), '02x')
        color_string += format(int(color_rgba.alpha * 255), '02x')
        return color_string
    
    def is_dark_theme():
        """Check if the current theme is dark"""
        return Adw.StyleManager.get_default().get_dark()


