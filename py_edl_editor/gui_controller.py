"""Main controller module for the GUI."""

# Import built-in modules
import os
import sys

# Import third-party modules
from PySide6 import QtWidgets

# Import local modules
from py_edl_editor.edl_parser import parse_edl
from py_edl_editor.cdl import ccc_xml

FRAMERATES = ["23.98", "24", "25", "29.97", "30", "50", "59.94", "60"]


class GuiController(object):
    """Main class for GuiController."""

    def __init__(self, gui):
        """Initialize controller class and connect to view.

        Args:
            gui (py_edl_editor.gui.PyEdlEditorApp): QT GUI Window.

        """
        self.gui = gui
        self.edl = None
        self.edl_path = ""
        self.fps = 24
        self.dest_folder = ""
        super(GuiController, self).__init__()

    def set_up_edl_view(self):
        """Set up the the EDL view."""
        if len(sys.argv) > 2: 
            edl_path = sys.argv[1]
            fps = sys.argv[2]
            if os.path.isfile(edl_path):
                self.edl_path = edl_path
            else:
                print("Cant find EDL File: {0}".format(edl_path))
            if fps in FRAMERATES:
                self.fps = fps
            else:
                self.fps = "24"
                print(f"Framerate invalid. Allowed framerates: {FRAMERATES}")
            self.gui.framerate.setCurrentIndex(FRAMERATES.index(self.fps))
        self.update_edl_view()
        
    def update_edl_view(self):
        """Update EDL table."""
        self.gui.setWindowTitle(
            f"EDL Editor [{os.path.split(self.edl_path)[1]}]"
        )
        self._set_edl()
        self._fill_edl_table()

    def update_framerate(self):
        """Update framerate based on selected GUI Dropdown value."""
        self.fps = self.gui.framerates[self.gui.framerate.currentIndex()]
        self.update_edl_view()

    def open_edl(self):
        """Open EDL File choseen in a File Dialog."""
        self.edl_path = QtWidgets.QFileDialog.getOpenFileName(
            caption='Open EDL', dir='.', filter='*.edl'
        )[0]
        self.update_edl_view()

    def switch_reel(self):
        """Switch EDL Reel and EDL Clip Name."""
        for event in self.edl.events:
            reel = event.reel
            event.reel = event.clip_name
            event.clip_name = reel
            self._fix_event_clip_name_comment(event)
        self._fill_edl_table()

    def toggle_frames_and_tc(self):
        """Toggle between showing SMPTE TCs and Frame numbers."""
        edl_table = self.gui.edl_view.edl_table
        edl_table.show_frames = not edl_table.show_frames
        self._fill_edl_table()

    def save_edl(self):
        """Save EDL (overwrite loaded EDL file)."""
        self._write_file(self.edl_path, [self.edl.to_string()])

    def save_edl_as(self):
        """Save EDL to user specified file path."""
        dest_file_path = QtWidgets.QFileDialog.getSaveFileName(
            caption='Save File As...', dir=self.edl_path
        )[0]
        self._write_file(dest_file_path, [self.edl.to_string()])

    def export_cdl(self):
        """Export CDLs as textfiles. CDL type based on GUI dropdown."""
        cdl_type = self.gui.cdl_type.currentText()
        self.dest_folder = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Choose folder', dir=self.edl_path
        )
        cdls = [event.cdl for event in self.edl.events]
        
        if cdl_type == ".ccc":
            basename = os.path.split(self.edl_path)[1].split(".")[0]
            filename = f"{basename}.ccc"
            dest_file_path = os.path.join(self.dest_folder, filename)
            self._write_file(dest_file_path, ccc_xml(cdls))
        else:
            for cdl in cdls:
                filename = f"{cdl.event.reel}{cdl_type}"
                dest_file_path = os.path.join(self.dest_folder, filename)
                if cdl_type == ".cdl":
                    self._write_file(dest_file_path, cdl.cdl_xml())
                else:
                    self._write_file(dest_file_path, cdl.cc_xml())

    def _fix_event_clip_name_comment(self, event):
        """Update EDL Event comment string that contains the Clip Name.

        When updating the clip_name value, the comment is not updated. But since
        we want to export the EDL, we need to update the comment.

        Args:
            event (Edl.event):  EDL Event instance.

        """
        for index, comment in enumerate(event.comments):
            if "* FROM CLIP NAME:" in comment:
                event.comments[index] = f"* FROM CLIP NAME: {event.clip_name}"

    def _write_file(self, dest_file_path, lines):
        """Write the givem lines to a text file."""
        with open(dest_file_path, 'w') as text_file:
            for line in lines:
                text_file.write(f"{line}\n")

    def _set_edl(self):
        """Parse and set the EDL."""
        self.edl = parse_edl(self.edl_path, self.fps)

    def _fill_edl_table(self):
        """Fill the EDL view with edl table events."""
        self.gui.edl_view.edl_table.clear()
        for event in self.edl.events:
            self.gui.edl_view.edl_table.add_edl_table_event(event)
        self.gui.edl_view.table.resizeColumnsToContents()
        self.gui.edl_view.table.resizeRowsToContents()