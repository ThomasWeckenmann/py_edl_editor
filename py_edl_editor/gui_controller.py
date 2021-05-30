"""Main controller module for the GUI."""

# Import built-in modules
import os
import subprocess
import sys

# Import third-party modules
from cdl_convert import collection, write  # type: ignore
from PySide2 import QtWidgets

# Import local modules
from py_edl_editor.cdl_tools import add_ccc_to_edl
from py_edl_editor.cdl_tools import add_cdls_to_edl
from py_edl_editor.edl_parser import parse_edl
from py_edl_editor.tc_tools import add_handles_to_edl
from py_edl_editor.tc_tools import remove_edl_gaps
from py_edl_editor.tc_tools import set_edl_start_tc

FRAMERATES = ["23.98", "24", "25", "29.97", "30", "50", "59.94", "60"]


# pylint: disable=too-many-public-methods
class GuiController:
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

    def set_up_edl_view(self):
        """Set up the the EDL view."""
        if len(sys.argv) > 1:
            edl_path = sys.argv[1]
            if len(sys.argv) > 2:
                fps = sys.argv[2]
            else:
                fps = "24"
            if os.path.isfile(edl_path):
                self.edl_path = edl_path
            else:
                print("Cant find EDL File: {0}".format(edl_path))
            if fps in FRAMERATES:
                self.fps = fps
            else:
                self.fps = "24"
                print(
                    "{0} {1}".format(
                        "Framerate invalid. Allowed framerates:",
                        FRAMERATES,
                    )
                )
            self.gui.framerate.setCurrentIndex(FRAMERATES.index(self.fps))
            self.update_edl_view()

    def update_edl_view(self):
        """Update EDL table."""
        self.gui.setWindowTitle(
            "EDL Editor [{0}]".format(os.path.split(self.edl_path)[1])
        )
        self._set_edl()
        self._fill_edl_table()

    def update_framerate(self):
        """Update framerate based on selected GUI Dropdown value."""
        self.fps = self.gui.framerates[self.gui.framerate.currentIndex()]
        self.update_edl_view()

    def open_edl(self):
        """Open EDL File choseen in a File Dialog."""
        edl_path = QtWidgets.QFileDialog.getOpenFileName(
            caption="Open EDL", dir=".", filter="*.edl"
        )[0]
        if edl_path:
            self.edl_path = edl_path
        self.update_edl_view()

    def reset_changes(self):
        """Reset all changes and go back to last saved state."""
        self.update_edl_view()

    def edit_edl_title(self):
        """Update the EDL title."""
        reply = QtWidgets.QInputDialog.getText(
            None, "Update EDL Title", "New EDL Title:"
        )
        if reply[1]:
            self.edl.title = reply[0]
        self.gui.edl_title.setText("EDL Title: {0}".format(self.edl.title))

    def switch_reel(self):
        """Switch EDL Reel and EDL Clip Name."""
        for event in self.edl.events:
            reel = event.reel
            event.reel = event.clip_name.replace(" ", "")
            event.clip_name = reel
            self._fix_event_clip_name_comment(event)
        self._fill_edl_table()

    def switch_reel_and_loc(self):
        """Switch EDL Reel and EDL Locator Name."""
        for event in self.edl.events:
            if event.has_locator:
                reel = event.reel
                event.reel = event.loc_name.replace(" ", "")
                event.loc_name = reel
                self._fix_event_locator_comment(event)
        self._fill_edl_table()

    def copy_source_file_to_reel(self):
        """Copy Source File to Reel."""
        for event in self.edl.events:
            event.reel = event.source_file
        self._fill_edl_table()

    def remove_reel_ext(self):
        """Remove extension from all reel names."""
        for event in self.edl.events:
            event.reel = os.path.splitext(event.reel)[0]
        self._fill_edl_table()

    def prepend_reels(self):
        """Prepend all reel names with user input string."""
        reply = QtWidgets.QInputDialog.getText(
            None, "Batch Edit Reels: Prepend String", "String to be prepended:"
        )
        if reply[1]:
            text = reply[0]
            for event in self.edl.events:
                event.reel = "{0}{1}".format(text, event.reel)
        self._fill_edl_table()

    def append_reels(self):
        """Append user input string to all reel names."""
        reply = QtWidgets.QInputDialog.getText(
            None, "Batch Edit Reels: Append String", "String to be appended:"
        )
        if reply[1]:
            text = reply[0]
            for event in self.edl.events:
                event.reel = "{0}{1}".format(event.reel, text)
        self._fill_edl_table()

    def replace_reels(self):
        """Replace string in all reel names."""
        reply = QtWidgets.QInputDialog.getText(
            None,
            "Batch Edit Reels | Replace String",
            "{0}{1}\n\n{2}".format(
                "String to be replaced followed by replacement string ",
                "(divided by comma)",
                "Example: 'old_value, new_value'",
            ),
        )
        if reply[1]:
            old_value, new_value = reply[0].split(",")
            for event in self.edl.events:
                event.reel = event.reel.replace(old_value, new_value.strip())
        self._fill_edl_table()

    def toggle_frames_and_tc(self):
        """Toggle between showing SMPTE TCs and Frame numbers."""
        edl_table = self.gui.edl_view.edl_table
        edl_table.show_frames = not edl_table.show_frames
        self._fill_edl_table()

    def save_edl(self):
        """Save EDL (overwrite loaded EDL file)."""
        for event in self.edl.events:
            self._fix_event_clip_name_comment(event)
        self._write_file(self.edl_path, [self.edl.to_string()])

    def save_edl_as(self):
        """Save EDL to user specified file path."""
        dest_file_path = QtWidgets.QFileDialog.getSaveFileName(
            caption="Save File As...", dir=self.edl_path
        )[0]
        self._write_file(dest_file_path, [self.edl.to_string()])
        self.edl_path = dest_file_path
        self.update_edl_view()

    def export_cdl(self):
        """Export CDLs as textfiles. CDL type based on GUI dropdown."""
        cdl_type = self.gui.cdl_type.currentText()
        self.dest_folder = QtWidgets.QFileDialog.getExistingDirectory(
            caption="Choose folder", dir=self.edl_path
        )
        cdls = []
        for event in self.edl.events:
            if event.cdl.has_sop and event.cdl.has_sat:
                cdls.append(event.cdl)
        if cdl_type == ".ccc":
            ccc = collection.ColorCollection()
            basename = os.path.split(self.edl_path)[1].split(".")[0]
            filename = "{0}.ccc".format(basename)
            # pylint: disable=protected-access
            ccc._file_out = os.path.join(self.dest_folder, filename)
            ccc.append_children(cdls)
            write.write_cc(ccc)
        else:
            for cdl in cdls:
                cdl.determine_dest(cdl_type[1:], self.dest_folder)
                if cdl_type == ".cdl":
                    write.write_cdl(cdl)
                if cdl_type == ".cc":
                    write.write_cc(cdl)

    def export_reels_txt(self):
        """Export all Reel Names to a textfile."""
        self.dest_folder = QtWidgets.QFileDialog.getExistingDirectory(
            caption="Choose folder", dir=self.edl_path
        )
        # pylint: disable=consider-using-set-comprehension
        reels = sorted(set([event.reel for event in self.edl.events]))
        basename = os.path.split(self.edl_path)[1].split(".")[0]
        file_path = os.path.join(self.dest_folder, "{0}.txt".format(basename))
        self._write_file(file_path, reels)

    def import_cdls(self):
        """Import CDLs and add it to the EDL event comments."""
        cdl_path = QtWidgets.QFileDialog.getOpenFileName(
            caption="Import CDLs", dir=self.edl_path, filter="*.c*"
        )[0]
        cdl_type = os.path.splitext(cdl_path)[1]
        if cdl_type == ".ccc":
            add_ccc_to_edl(self.edl, cdl_path)
        elif cdl_type in [".cdl", ".cc"]:
            cdl_files = []
            for file in os.listdir(os.path.dirname(cdl_path)):
                if file.endswith(cdl_type):
                    cdl_file = os.path.join(os.path.dirname(cdl_path), file)
                    cdl_files.append(cdl_file)
            add_cdls_to_edl(self.edl, cdl_type, cdl_files)
        else:
            print("Wrong file type. Supported types: .cdl, .cc, .ccc")
        self._fill_edl_table()

    def remove_gaps(self):
        """Remove EDL gaps."""
        self.edl = remove_edl_gaps(self.edl)
        self._fill_edl_table()

    def set_start_tc(self):
        """Set start TC to user input value."""
        reply = QtWidgets.QInputDialog.getText(
            None,
            "Set EDL Start Timecode",
            "Start TC (either in Frame Numbers or SMPTE TC):",
        )
        if reply[1]:
            self.edl = set_edl_start_tc(self.edl, reply[0])
            self._fill_edl_table()

    def add_handles(self):
        """Add handles (user input value) to all edl events."""
        reply = QtWidgets.QInputDialog.getText(
            None, "Add Head and Tail Handles", "Number of handles:"
        )
        if reply[1]:
            self.edl = add_handles_to_edl(self.edl, int(reply[0]))
            self._fill_edl_table()

    def show_otio_timeline(self):
        """Open EDL as open timeline io view."""
        subprocess.Popen(["otioview", "{0}".format(self.edl_path)])

    def _set_edl(self):
        """Parse and set the EDL."""
        self.edl = parse_edl(self.edl_path, self.fps)
        self.gui.edl_title.setText("EDL Title: {0}".format(self.edl.title))

    def _fill_edl_table(self):
        """Fill the EDL view with edl table events."""
        self.gui.edl_view.edl_table.clear()
        for event in self.edl.events:
            self.gui.edl_view.edl_table.add_edl_table_event(event)
        self.gui.edl_view.table.resizeColumnsToContents()
        self.gui.edl_view.table.resizeRowsToContents()

    @classmethod
    def _fix_event_clip_name_comment(cls, event):
        """Update EDL Event comment string that contains the Clip Name.

        When updating the clip_name value, the comment is not updated. But
        since we want to export the EDL, we need to update the comment.

        Args:
            event (Edl.event):  EDL Event instance.

        """
        for index, comment in enumerate(event.comments):
            if "* FROM CLIP NAME:" in comment:
                event.comments[index] = "{0} {1}".format(
                    "* FROM CLIP NAME:", event.clip_name
                )

    @classmethod
    def _fix_event_locator_comment(cls, event):
        """Update EDL Event comment string that contains the Locator.

        When updating the clip_name value, the comment is not updated. But
        since we want to export the EDL, we need to update the comment.

        Args:
            event (Edl.event):  EDL Event instance.

        """
        for index, comment in enumerate(event.comments):
            if "* LOC:" in comment:
                event.comments[index] = "* LOC: {0} {1} {2}".format(
                    event.loc_tc, event.loc_color, event.loc_name
                )

    @classmethod
    def _write_file(cls, dest_file_path, lines):
        """Write the givem lines to a text file."""
        with open(dest_file_path, "w") as text_file:
            for line in lines:
                text_file.write("{0}\n".format(line))
