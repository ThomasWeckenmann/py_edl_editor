"""Main Window."""

# Import built-in modules
import sys

# Import third-party modules
from PySide6 import QtCore  
from PySide6 import QtWidgets

# Import local modules
from py_edl_editor.edl_table import EdlTable
from py_edl_editor.edl_table import ReelDelegate
from py_edl_editor.gui_controller import GuiController
from py_edl_editor.gui_controller import FRAMERATES


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
        self.setMinimumWidth(1400)
        self.setMinimumHeight(600)

        # Set up main box layouts
        layout = QtWidgets.QHBoxLayout()
        layout_left = QtWidgets.QVBoxLayout()
        layout_right = QtWidgets.QVBoxLayout()

        # Set up form layouts
        self.input_layout_left = QtWidgets.QFormLayout()
        self.display_layout_left = QtWidgets.QFormLayout()
        self.tools_layout_left = QtWidgets.QFormLayout()
        self.output_layout_left = QtWidgets.QFormLayout()
        self.form_layout_right = QtWidgets.QFormLayout()
        
        # Set up group boxes on the left
        input_group_box = QtWidgets.QGroupBox("Input")
        display_group_box = QtWidgets.QGroupBox("Display")
        tools_group_box = QtWidgets.QGroupBox("Tools")
        output_group_box = QtWidgets.QGroupBox("Output")
        
        # Show group boxes
        self._input_group_elements()
        self._display_group_elements()
        self._tools_group_elements()
        self._output_group_elements()
        self._edl_group_elements()
        
        # Set up box layouts
        input_vbox = QtWidgets.QVBoxLayout()
        display_vbox = QtWidgets.QVBoxLayout()
        tools_vbox = QtWidgets.QVBoxLayout()
        output_vbox = QtWidgets.QVBoxLayout()
        
        # Add layouts to the box layouts
        input_vbox.addLayout(self.input_layout_left)
        display_vbox.addLayout(self.display_layout_left)
        tools_vbox.addLayout(self.tools_layout_left)
        output_vbox.addLayout(self.output_layout_left)
        
        # Set layout for group boxes
        input_group_box.setLayout(input_vbox)
        display_group_box.setLayout(display_vbox)
        tools_group_box.setLayout(tools_vbox)
        output_group_box.setLayout(output_vbox)

        # Add group boxes to the layouts
        layout_left.addWidget(input_group_box)
        layout_left.addWidget(display_group_box)
        layout_left.addWidget(tools_group_box)
        layout_left.addWidget(output_group_box)
        layout_right.addWidget(self.edl_view)
        
        # Set up main layout
        layout.addLayout(layout_left)
        layout.addLayout(layout_right)
        self.setLayout(layout)

    def _input_group_elements(self):
        """Show elements of the input group."""

        # EDL Title
        self.edl_title = QtWidgets.QLabel("", self)
        self.input_layout_left.addRow(self.edl_title)

        # FPS Dropdown
        framerate_label = QtWidgets.QLabel("FPS:", self)
        self.framerate = QtWidgets.QComboBox(self) 
        self.framerates = FRAMERATES
        self.framerate.addItems(self.framerates)
        self.input_layout_left.addRow(framerate_label, self.framerate)
        self.framerate.currentIndexChanged.connect(
            self.controller.update_framerate
        )

        # Open EDL Button
        select_edl_button_box = QtWidgets.QHBoxLayout()
        select_edl_button = QtWidgets.QPushButton("Open EDL", self)
        select_edl_button_box.addWidget(select_edl_button)
        self.input_layout_left.addRow(select_edl_button_box)
        select_edl_button.clicked.connect(self.controller.open_edl)

        # Reset changes
        reset_changes_button = QtWidgets.QPushButton("Reset changes", self)
        self.input_layout_left.addRow(reset_changes_button)
        reset_changes_button.clicked.connect(self.controller.reset_changes)

    def _display_group_elements(self):
        """Show elements of the display group."""

        # Show Frames instead of TC
        toggle_frames_and_tc_button = QtWidgets.QPushButton(
            "Show Frames instead of TC", self
        )
        self.display_layout_left.addRow(toggle_frames_and_tc_button)
        toggle_frames_and_tc_button.clicked.connect(
            self.controller.toggle_frames_and_tc
        )    

    def _tools_group_elements(self):
        """Show elements of the tool group."""

        # Edit EDL Title
        edit_edl_title_button = QtWidgets.QPushButton("Edit EDL Title", self)
        self.tools_layout_left.addRow(edit_edl_title_button)
        edit_edl_title_button.clicked.connect(self.controller.edit_edl_title)

        # Switch Reel and Clip Name Button
        switch_reel_button = QtWidgets.QPushButton(
            "Switch Reel and Clip Name", self
        )
        self.tools_layout_left.addRow(switch_reel_button)
        switch_reel_button.clicked.connect(self.controller.switch_reel)

        # Copy Source File to Reel
        copy_source_file_to_reel_button = QtWidgets.QPushButton(
            "Copy Source File to Reel", self
        )
        self.tools_layout_left.addRow(copy_source_file_to_reel_button)
        copy_source_file_to_reel_button.clicked.connect(
            self.controller.copy_source_file_to_reel
        )

        # Remove extension from reels
        remove_reel_ext_button = QtWidgets.QPushButton(
            "Remove extension from Reels", self
        )
        self.tools_layout_left.addRow(remove_reel_ext_button)
        remove_reel_ext_button.clicked.connect(self.controller.remove_reel_ext)

        # Batch Edit Reels
        batch_edit_reels_label = QtWidgets.QLabel("Reels:", self)
        prepend_reels_button = QtWidgets.QPushButton("Prepend", self)
        append_reels_button = QtWidgets.QPushButton("Append", self)
        replace_reels_button = QtWidgets.QPushButton("Replace", self)
        batch_edit_reels_hbox = QtWidgets.QHBoxLayout()
        batch_edit_reels_hbox.addWidget(batch_edit_reels_label)
        batch_edit_reels_hbox.addWidget(prepend_reels_button)
        batch_edit_reels_hbox.addWidget(append_reels_button)
        batch_edit_reels_hbox.addWidget(replace_reels_button)
        self.tools_layout_left.addRow(batch_edit_reels_hbox)
        prepend_reels_button.clicked.connect(self.controller.prepend_reels)
        append_reels_button.clicked.connect(self.controller.append_reels)
        replace_reels_button.clicked.connect(self.controller.replace_reels)

    def _output_group_elements(self):
        """Show elements of the output group."""

        # Save EDL Buttons
        save_edl_button = QtWidgets.QPushButton("Save EDL", self)
        save_edl_as_button = QtWidgets.QPushButton("Save EDL As...", self)
        self.output_layout_left.addRow(save_edl_button)
        self.output_layout_left.addRow(save_edl_as_button)
        save_edl_button.clicked.connect(self.controller.save_edl)
        save_edl_as_button.clicked.connect(self.controller.save_edl_as)

        # Export CDL
        export_cdl_button = QtWidgets.QPushButton("Export CDLs", self)
        self.cdl_type = QtWidgets.QComboBox(self) 
        cdl_types = [".ccc", ".cc", ".cdl"]
        self.cdl_type.addItems(cdl_types)
        self.output_layout_left.addRow(export_cdl_button, self.cdl_type)
        export_cdl_button.clicked.connect(self.controller.export_cdl)    

    def _edl_group_elements(self):
        """Show the EDL tablee."""
        self.edl_view = EdlEditor()
        self.controller.set_up_edl_view()

    def run(self, qt_app):
        """Run the QT App.

        Args:
            qt_app (QtWidgets.QApplication): QT App.

        """
        self.show()
        qt_app.exec_()

class EdlEditor(QtWidgets.QWidget):
    """View element containing the EDL table."""

    def __init__(self):
        """Initialize the EdlEditor instance."""
        super(EdlEditor, self).__init__()

        asset_model = QtCore.QSortFilterProxyModel()
        asset_model.setSourceModel(EdlTable())

        self.table = QtWidgets.QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(asset_model)
        self.table.verticalHeader().hide()
        self.table.setItemDelegateForColumn(1, ReelDelegate(self.table))
        self.table.setItemDelegateForColumn(2, ReelDelegate(self.table))
        self.edl_table = self.table.model().sourceModel()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)


class PyEdlEditorGui(object):
    """Construct QApplication used for the GUI."""

    def __init__(self):
        """Initialize the Gui instance."""
        qt_app = QtWidgets.QApplication(sys.argv)
        app = PyEdlEditorApp(qt_app)
        app.run(qt_app)
