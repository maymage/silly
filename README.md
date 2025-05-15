# Silktex

A simple and modern LaTeX editor for the Gnome desktop, written in Python with Gtk/Adwaita.

![Screenshot](https://handbook.gnome.org/_images/handbook.svg)

## Running Silktex on Debian based Distributions

1. Run the following command to install prerequisite Debian packages:<br />
`apt-get install meson python3-gi gir1.2-gtk-4.0 gir1.2-gtksource-5 gir1.2-pango-1.0 gir1.2-poppler-0.18 gir1.2-webkit-6.0 gettext python3-cairo python3-gi-cairo python3-pexpect gir1.2-adw-1 python3-bibtexparser python3-willow python3-numpy gir1.2-xdp-1.0`

2. Download und Unpack Silktex from GitHub

3. cd to the Silktex folder

4. Run meson: `meson builddir`<br />

Note: Some distributions may not include systemwide installations of Python modules which aren't installed from distribution packages. In this case, you want to install Silktex in your home directory with `meson builddir --prefix=~/.local`.

5. Install Silktex with: `ninja install -C builddir`<br />
Or run it locally: `./main.py`

## Building your documents from within the app

To build your documents from within the app you have to install a LaTeX interpreter. For example if you want to build with XeLaTeX, on Debian this can be installed like so:
`apt-get install texlive-xetex`

To specify a build command open the "Preferences" dialog and choose the command you want to use under "LaTeX Interpreter".

## Getting in touch

Silktex development / discussion takes place on GitHub at [https://github.com/DERK0CHER/silly/edit/master/README](https://github.com/DERK0CHER/silly/).

## Acknowledgements

Silktex is a hard fork of [Setzer](https://github.com/cvfosammmm/Setzer), whose development had be somewhat dorment for some time.  

## License

Silktex is licensed under GPL version 3 or later. See the COPYING file for details.
