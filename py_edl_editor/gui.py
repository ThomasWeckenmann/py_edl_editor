"""Main Window."""

# Import built-in modules
import sys

# Import third-party modules
from PySide2 import QtCore
from PySide2 import QtWidgets

# Import local modules
from py_edl_editor.edl_table import EdlTable
from py_edl_editor.edl_table import EditableDelegate
from py_edl_editor.gui_controller import GuiController
from py_edl_editor.gui_controller import FRAMERATES


# pylint: disable=maybe-no-member
# pylint: disable=too-many-instance-attributes,too-many-locals
# pylint: disable=too-many-statements,too-few-public-methods
class PyEdlEditorApp(QtWidgets.QWidget):
    """Main Class for the GUI."""

    def __init__(self, qt_app):
        """Initialize the PyEdlEditorApp instance.

        Args:
            qt_app (QtWidgets.QApplication): QApplication.

        """
        QtWidgets.QWidget.__init__(self)
        self.qt_app = qt_app
        self.controller = GuiController(self)
        self.setWindowTitle("EDL Editor")
        self.setMinimumWidth(1500)
        self.setMinimumHeight(800)

        # Set up main box layouts
        layout = QtWidgets.QHBoxLayout()
        layout_left = QtWidgets.QVBoxLayout()
        layout_middle = QtWidgets.QVBoxLayout()
        layout_right = QtWidgets.QVBoxLayout()

        # Set up form layouts
        self.input_layout = QtWidgets.QFormLayout()
        self.tools_layout = QtWidgets.QFormLayout()
        self.output_layout = QtWidgets.QFormLayout()
        self.edl_table_layout = QtWidgets.QFormLayout()
        self.display_layout = QtWidgets.QFormLayout()
        self.timecode_tools_layout = QtWidgets.QFormLayout()

        # Set up group boxes on the left
        input_group_box = QtWidgets.QGroupBox("Input")
        display_group_box = QtWidgets.QGroupBox("Display")
        text_tools_group_box = QtWidgets.QGroupBox("Text Tools")
        output_group_box = QtWidgets.QGroupBox("Output")
        timecode_tools_group_box = QtWidgets.QGroupBox("Timecode Tools")

        # Show group boxes
        self._input_group_elements()
        self._display_group_elements()
        self._text_tools_group_elements()
        self._output_group_elements()
        self._edl_group_elements()
        self._timecode_tools_group_elements()

        # Set up vbox layouts
        input_vbox = QtWidgets.QVBoxLayout()
        display_vbox = QtWidgets.QVBoxLayout()
        text_tools_vbox = QtWidgets.QVBoxLayout()
        output_vbox = QtWidgets.QVBoxLayout()
        timecode_tools_vbox = QtWidgets.QVBoxLayout()

        # Add layouts to the box layouts
        input_vbox.addLayout(self.input_layout)
        display_vbox.addLayout(self.display_layout)
        text_tools_vbox.addLayout(self.tools_layout)
        output_vbox.addLayout(self.output_layout)
        timecode_tools_vbox.addLayout(self.timecode_tools_layout)

        # Set layout for group boxes
        input_group_box.setLayout(input_vbox)
        display_group_box.setLayout(display_vbox)
        text_tools_group_box.setLayout(text_tools_vbox)
        output_group_box.setLayout(output_vbox)
        timecode_tools_group_box.setLayout(timecode_tools_vbox)

        # Add group boxes to the layouts
        layout_left.addWidget(input_group_box)
        layout_left.addWidget(text_tools_group_box)
        layout_left.addWidget(output_group_box)
        layout_middle.addWidget(self.edl_view)
        layout_right.addWidget(display_group_box)
        layout_right.addWidget(timecode_tools_group_box)

        # Set up main layout
        layout.addLayout(layout_left)
        layout.addLayout(layout_middle)
        layout.addLayout(layout_right)
        self.setLayout(layout)

    def _input_group_elements(self):
        """Show elements of the input group."""

        # EDL Title
        self.edl_title = QtWidgets.QLabel("", self)
        self.input_layout.addRow(self.edl_title)

        # FPS Dropdown
        framerate_label = QtWidgets.QLabel("FPS:", self)
        self.framerate = QtWidgets.QComboBox(self)
        self.framerates = FRAMERATES
        self.framerate.addItems(self.framerates)
        self.input_layout.addRow(framerate_label, self.framerate)
        self.framerate.currentIndexChanged.connect(
            self.controller.update_framerate
        )  # noqa: E501

        # Open EDL Button
        select_edl_button_box = QtWidgets.QHBoxLayout()
        select_edl_button = QtWidgets.QPushButton("Open EDL", self)
        select_edl_button_box.addWidget(select_edl_button)
        self.input_layout.addRow(select_edl_button_box)
        select_edl_button.clicked.connect(self.controller.open_edl)

        # Import CDLs Button
        import_cdl_button = QtWidgets.QPushButton("Import CDLs", self)
        self.input_layout.addRow(import_cdl_button)
        import_cdl_button.clicked.connect(self.controller.import_cdls)

        # Reset changes
        reset_changes_button = QtWidgets.QPushButton("Reset changes", self)
        self.input_layout.addRow(reset_changes_button)
        reset_changes_button.clicked.connect(self.controller.reset_changes)

    def _display_group_elements(self):
        """Show elements of the display group."""

        # Show Frames instead of TC
        toggle_frames_and_tc_button = QtWidgets.QPushButton(
            "Show Frames instead of TC", self
        )
        self.display_layout.addRow(toggle_frames_and_tc_button)
        toggle_frames_and_tc_button.clicked.connect(
            self.controller.toggle_frames_and_tc
        )

        # Show OTIO Timeline
        show_otio_button = QtWidgets.QPushButton("Show OTIO Timeline", self)
        self.display_layout.addRow(show_otio_button)
        show_otio_button.clicked.connect(self.controller.show_otio_timeline)

    def _text_tools_group_elements(self):
        """Show elements of the tool group."""

        # Edit EDL Title
        edit_edl_title_button = QtWidgets.QPushButton("Edit EDL Title", self)
        self.tools_layout.addRow(edit_edl_title_button)
        edit_edl_title_button.clicked.connect(self.controller.edit_edl_title)

        # Switch Reel and Clip Name Button
        switch_reel_button = QtWidgets.QPushButton(
            "Switch Reel and Clip Name", self
        )  # noqa: E501
        self.tools_layout.addRow(switch_reel_button)
        switch_reel_button.clicked.connect(self.controller.switch_reel)

        # Switch Reel and Locator Name Button
        switch_reel_loc_button = QtWidgets.QPushButton(
            "Switch Reel and Locator Name", self
        )
        self.tools_layout.addRow(switch_reel_loc_button)
        switch_reel_loc_button.clicked.connect(
            self.controller.switch_reel_and_loc
        )  # noqa: E501

        # Copy Source File to Reel
        copy_source_file_to_reel_button = QtWidgets.QPushButton(
            "Copy Source File to Reel", self
        )
        self.tools_layout.addRow(copy_source_file_to_reel_button)
        copy_source_file_to_reel_button.clicked.connect(
            self.controller.copy_source_file_to_reel
        )

        # Remove extension from reels
        remove_reel_ext_button = QtWidgets.QPushButton(
            "Remove extension from Reels", self
        )
        self.tools_layout.addRow(remove_reel_ext_button)
        remove_reel_ext_button.clicked.connect(self.controller.remove_reel_ext)

        # Batch Edit Reels
        batch_edit_reels_label = QtWidgets.QLabel("Reels:", self)
        prepend_reels_button = QtWidgets.QPushButton("Prepend", self)
        append_reels_button = QtWidgets.QPushButton("Append", self)
        replace_reels_button = QtWidgets.QPushButton("Replace", self)
        batch_edit_reels_hbox = QtWidgets.QHBoxLayout()
        batch_edit_reels_hbox.addWidget(prepend_reels_button)
        batch_edit_reels_hbox.addWidget(append_reels_button)
        batch_edit_reels_hbox.addWidget(replace_reels_button)
        self.tools_layout.addRow(batch_edit_reels_label)
        self.tools_layout.addRow(batch_edit_reels_hbox)
        prepend_reels_button.clicked.connect(self.controller.prepend_reels)
        append_reels_button.clicked.connect(self.controller.append_reels)
        replace_reels_button.clicked.connect(self.controller.replace_reels)

    def _output_group_elements(self):
        """Show elements of the output group."""

        # Save EDL Buttons
        save_edl_button = QtWidgets.QPushButton("Save EDL", self)
        save_edl_as_button = QtWidgets.QPushButton("Save EDL As...", self)
        self.output_layout.addRow(save_edl_button)
        self.output_layout.addRow(save_edl_as_button)
        save_edl_button.clicked.connect(self.controller.save_edl)
        save_edl_as_button.clicked.connect(self.controller.save_edl_as)

        # Export CDL
        export_cdl_button = QtWidgets.QPushButton("Export CDLs", self)
        self.cdl_type = QtWidgets.QComboBox(self)
        cdl_types = [".ccc", ".cc", ".cdl"]
        self.cdl_type.addItems(cdl_types)
        self.output_layout.addRow(export_cdl_button, self.cdl_type)
        export_cdl_button.clicked.connect(self.controller.export_cdl)

        # Save Textfile Button
        export_reels_txt_button = QtWidgets.QPushButton(
            "Export Reels to Textfile", self
        )
        self.output_layout.addRow(export_reels_txt_button)
        export_reels_txt_button.clicked.connect(
            self.controller.export_reels_txt
        )  # noqa: E501

    def _edl_group_elements(self):
        """Show the EDL table."""
        self.edl_view = EdlEditor()
        self.controller.set_up_edl_view()

    def _timecode_tools_group_elements(self):
        """Show the timecode tools."""
        remove_gaps_button = QtWidgets.QPushButton("Remove Gaps", self)
        set_start_tc_button = QtWidgets.QPushButton("Set Start TC", self)
        add_handles_button = QtWidgets.QPushButton("Add Handles", self)
        self.timecode_tools_layout.addRow(remove_gaps_button)
        self.timecode_tools_layout.addRow(set_start_tc_button)
        self.timecode_tools_layout.addRow(add_handles_button)
        remove_gaps_button.clicked.connect(self.controller.remove_gaps)
        set_start_tc_button.clicked.connect(self.controller.set_start_tc)
        add_handles_button.clicked.connect(self.controller.add_handles)

    def run(self, qt_app):
        """Run the QT App.

        Args:
            qt_app (QtWidgets.QApplication): QT App.

        """
        self.show()
        qt_app.exec_()


class EdlEditor(QtWidgets.QWidget):
    """View element containing the EDL table."""

    # pylint: disable=super-with-arguments
    def __init__(self):
        """Initialize the EdlEditor instance."""
        super(EdlEditor, self).__init__()

        asset_model = QtCore.QSortFilterProxyModel()
        asset_model.setSourceModel(EdlTable())

        self.table = QtWidgets.QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(asset_model)
        self.table.verticalHeader().hide()
        self.table.setItemDelegateForColumn(1, EditableDelegate(self.table))
        self.table.setItemDelegateForColumn(2, EditableDelegate(self.table))
        self.edl_table = self.table.model().sourceModel()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)


class PyEdlEditorGui:
    """Construct QApplication used for the GUI."""

    def __init__(self):
        """Initialize the Gui instance."""
        qt_app = QtWidgets.QApplication(sys.argv)
        app = PyEdlEditorApp(qt_app)
        app.run(qt_app)
