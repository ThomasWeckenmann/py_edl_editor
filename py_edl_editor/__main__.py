"""Shows the EDL Viewer GUI."""

# Import built-in modules
import os
import platform

# Import local modules
from py_edl_editor.gui import PyEdlEditorGui


def main():
    """Run py_edl_editor."""
    # Add ENV for Big Sur Issue
    # https://stackoverflow.com/questions/64818879/is-there-any-solution-regarding-to-pyqt-library-doesnt-work-in-mac-os-big-sur/64856281
    if platform.system() == "Darwin":
        os.environ["QT_MAC_WANTS_LAYER"] = "1"
    PyEdlEditorGui()


if __name__ == "__main__":
    main()
