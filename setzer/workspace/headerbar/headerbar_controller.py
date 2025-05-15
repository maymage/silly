        # connect signals
        view.symbols_toggle.connect('toggled', self.on_symbols_toggle_toggled)
        view.document_structure_toggle.connect('toggled', self.on_document_structure_toggle_toggled)
        view.preview_toggle.connect('toggled', self.on_preview_toggle_toggled)
        view.help_toggle.connect('toggled', self.on_help_toggle_toggled)
        
        # Set up theme mode action
        self.init_theme_actions()
