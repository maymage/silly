#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import traceback

# Add basic debug output
print("Starting Setzer...")

try:
    # Force X11 backend to avoid Wayland protocol errors during development
    os.environ.setdefault('GDK_BACKEND', 'x11')
    print("Set GDK_BACKEND to x11")

    import gi
    import gettext
    import argparse

    print("Imports successful")

    # Projekt-Root ermitteln und ins Modul-Suchpath aufnehmen
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, PROJECT_ROOT)
    print(f"Project root: {PROJECT_ROOT}")

    # GTK/Adwaita Versionen
    print("Loading GTK and Adwaita...")
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Gio, Adw, GLib
    print("GTK and Adwaita loaded")

    # Setzer-Module imports
    print("Importing Setzer modules...")
    from setzer.workspace.workspace import Workspace
    import setzer.workspace.workspace_viewgtk as view
    import setzer.keyboard_shortcuts.shortcuts as shortcuts
    from setzer.app.service_locator import ServiceLocator
    from setzer.dialogs.dialog_locator import DialogLocator
    from setzer.app.color_manager import ColorManager
    from setzer.app.font_manager import FontManager
    from setzer.popovers.popover_manager import PopoverManager
    from setzer.app.latex_db import LaTeXDB
    from setzer.settings.document_settings import DocumentSettings
    from setzer.helpers.timer import timer
    print("Setzer modules imported")

    class MainApplicationController(Adw.Application):

        def __init__(self):
            print("Initializing MainApplicationController...")
            super().__init__(application_id='org.cvfosammmm.Setzer', flags=Gio.ApplicationFlags.NON_UNIQUE)
            self.is_active = False

            # Connect to the activate signal
            self.connect('activate', self.on_activate)
            print("MainApplicationController initialized")

        def on_activate(self, app):
            print("on_activate signal handler called")
            self.activate_app()

        def do_activate(self):
            print("do_activate called")
            self.activate_app()

        def activate_app(self):
            print("activate_app called")
            if self.is_active:
                print("Already active, returning")
                return

            self.is_active = True

            # Pfade für Übersetzungen und Assets
            localedir = os.path.join(PROJECT_ROOT, 'po')
            resources_path = os.path.join(PROJECT_ROOT, 'data', 'resources')
            app_icons_path = os.path.join(PROJECT_ROOT, 'data')
            print(f"Resources path: {resources_path}")

            # gettext initialisieren
            print("Initializing gettext...")
            gettext.install('setzer', names=('ngettext',), localedir=localedir)
            print("gettext initialized")

            # Einstellungen und Theme
            print("Loading settings...")
            self.settings = ServiceLocator.get_settings()
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            print("Settings loaded")

            # ServiceLocator konfigurieren
            print("Configuring ServiceLocator...")
            ServiceLocator.set_setzer_version('@setzer_version@')
            ServiceLocator.set_resources_path(resources_path)
            ServiceLocator.set_app_icons_path(app_icons_path)
            print("ServiceLocator configured")

            # Hauptfenster, Model und Dialoge initialisieren
            print("Creating main window...")
            self.main_window = view.MainWindow(self)
            print("Main window created")

            print("Setting up icon theme...")
            icon_theme = Gtk.IconTheme.get_for_display(self.main_window.get_display())
            icon_theme.add_search_path(os.path.join(resources_path, 'icons'))
            icon_theme.add_search_path(app_icons_path)
            for folder in ['arrows', 'greek_letters', 'misc_math', 'misc_text', 'operators', 'relations']:
                icon_theme.add_search_path(os.path.join(resources_path, 'symbols', folder))
            print("Icon theme set up")

            print("Initializing managers...")
            ServiceLocator.set_main_window(self.main_window)
            ColorManager.init(self.main_window)
            FontManager.init(self.main_window)
            print("Managers initialized")

            print("Creating workspace...")
            self.workspace = Workspace()
            PopoverManager.init(self.main_window, self.workspace)
            print("Initializing LaTeXDB...")
            try:
                LaTeXDB.init(resources_path)
                print("LaTeXDB initialized")
            except Exception as e:
                print(f"Error initializing LaTeXDB: {str(e)}")
                print("Continuing without LaTeXDB...")

            print("Creating widgets...")
            self.main_window.create_widgets()
            ServiceLocator.set_workspace(self.workspace)

            print("Initializing dialogs...")
            try:
                DialogLocator.init_dialogs(self.main_window, self.workspace)
                print("Dialogs initialized")
            except Exception as e:
                print(f"Error initializing dialogs: {str(e)}")
                print("Continuing without dialogs...")

            # Fensterzustand wiederherstellen und anzeigen
            print("Restoring window state...")
            if self.settings.get_value('window_state', 'is_maximized'):
                self.main_window.maximize()
            else:
                self.main_window.unmaximize()
            width = self.settings.get_value('window_state', 'width')
            height = self.settings.get_value('window_state', 'height')
            self.main_window.set_default_size(width, height)

            # Signale verbinden
            print("Connecting signals...")
            self.main_window.connect('close-request', self.on_window_close)
            print("Signals connected")

            # Controller und Shortcuts
            print("Initializing workspace controller...")
            try:
                self.workspace.init_workspace_controller()
                self.shortcuts = shortcuts.Shortcuts()
                print("Workspace controller initialized")
            except Exception as e:
                print(f"Error initializing workspace controller: {str(e)}")

            print("Presenting window...")
            # Try to ensure the window is presented by scheduling it on the main loop
            GLib.idle_add(self.present_window)
            print("Activation scheduled")

        def present_window(self):
            print("Presenting window now...")
            self.main_window.present()
            print("Window presented")
            return False  # Don't call again

        # Signal-Handler implementieren
        def on_window_close(self, window, parameter=None):
            print("Window close requested")
            self.save_quit()
            return True

        def on_quit_action(self, action, parameter=None):
            print("Quit action triggered")
            self.save_quit()

        # Bestehende Methoden: save_quit, save_quit_callback, save_callback, save_state_and_quit
        def save_quit(self):
            print("Saving and quitting...")
            # Implement your save and quit logic here
            print("Application should now quit")
            self.quit()

    if __name__ == '__main__':
        print("Creating main controller...")
        main_controller = MainApplicationController()
        print("Running application...")
        exit_status = main_controller.run(sys.argv)
        print(f"Application exited with status: {exit_status}")
        sys.exit(exit_status)

except Exception as e:
    print(f"Error: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)
