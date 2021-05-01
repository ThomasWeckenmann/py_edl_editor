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

        # Main Layout.
        self.layout = QtWidgets.QHBoxLayout()
        self.layout_left = QtWidgets.QVBoxLayout()
        self.layout_right = QtWidgets.QVBoxLayout()

        # Form Layouts Left.
        self.input_layout_left = QtWidgets.QFormLayout()
        self.tools_layout_left = QtWidgets.QFormLayout()
        self.output_layout_left = QtWidgets.QFormLayout()
        
        # Input Group on the left
        self.input_group_box = QtWidgets.QGroupBox("Input")

        # FPS Dropdown
        self.framerate_label = QtWidgets.QLabel("FPS:", self)
        self.framerate = QtWidgets.QComboBox(self) 
        self.framerates = FRAMERATES
        self.framerate.addItems(self.framerates)
        self.input_layout_left.addRow(self.framerate_label, self.framerate)
        self.framerate.currentIndexChanged.connect(
            self.controller.update_framerate
        )

        # Open EDL Button
        self.select_edl_button_box = QtWidgets.QHBoxLayout()
        self.select_edl_button = QtWidgets.QPushButton("Open EDL", self)
        self.select_edl_button_box.addWidget(self.select_edl_button)
        self.input_layout_left.addRow(self.select_edl_button_box)
        self.select_edl_button.clicked.connect(self.controller.open_edl)
        
        # Tools Group on the left
        self.tools_group_box = QtWidgets.QGroupBox("Tools")
        
        # Switch Reel and Clip Name Button
        self.switch_reel_button = QtWidgets.QPushButton(
            "Switch Reel and Clip Name", self
        )
        self.tools_layout_left.addRow(self.switch_reel_button)
        self.switch_reel_button.clicked.connect(self.controller.switch_reel)
        
        # Remove extension from reels
        self.remove_reel_ext_button = QtWidgets.QPushButton(
            "Remove extension from Reels", self
        )
        self.tools_layout_left.addRow(self.remove_reel_ext_button)
        self.remove_reel_ext_button.clicked.connect(
            self.controller.remove_reel_ext
        )
        
        # Show Frames instead of TC
        self.toggle_frames_and_tc_button = QtWidgets.QPushButton(
            "Show Frames instead of TC", self
        )
        self.tools_layout_left.addRow(self.toggle_frames_and_tc_button)
        self.toggle_frames_and_tc_button.clicked.connect(
            self.controller.toggle_frames_and_tc
        )

        # Batch Edit Reels
        batch_edit_reels_label = QtWidgets.QLabel("Batch Edit Reels:", self)
        prepend_reels_button = QtWidgets.QPushButton("Prepend", self)
        append_reels_button = QtWidgets.QPushButton("Append", self)
        replace_reels_button = QtWidgets.QPushButton("Replace", self)
        batch_edit_reels_hbox = QtWidgets.QHBoxLayout()
        batch_edit_reels_hbox.addWidget(prepend_reels_button)
        batch_edit_reels_hbox.addWidget(append_reels_button)
        batch_edit_reels_hbox.addWidget(replace_reels_button)
        self.tools_layout_left.addRow(batch_edit_reels_label)
        self.tools_layout_left.addRow(batch_edit_reels_hbox)
        prepend_reels_button.clicked.connect(self.controller.prepend_reels)
        append_reels_button.clicked.connect(self.controller.append_reels)
        replace_reels_button.clicked.connect(self.controller.replace_reels)

        # Output Group on the left
        self.output_group_box = QtWidgets.QGroupBox("Output")
        
        # Save EDL Buttons
        self.save_edl_button = QtWidgets.QPushButton("Save EDL", self)
        self.save_edl_as_button = QtWidgets.QPushButton("Save EDL As...", self)
        self.output_layout_left.addRow(self.save_edl_button)
        self.output_layout_left.addRow(self.save_edl_as_button)
        self.save_edl_button.clicked.connect(self.controller.save_edl)
        self.save_edl_as_button.clicked.connect(self.controller.save_edl_as)

        # Export CDL
        self.export_cdl_button = QtWidgets.QPushButton("Export CDLs", self)
        self.cdl_type = QtWidgets.QComboBox(self) 
        self.cdl_types = [".ccc", ".cc", ".cdl"]
        self.cdl_type.addItems(self.cdl_types)
        self.output_layout_left.addRow(self.export_cdl_button, self.cdl_type)
        self.export_cdl_button.clicked.connect(self.controller.export_cdl)
        
        # Form Layout Right.
        self.form_layout_right = QtWidgets.QFormLayout()

        # EDL
        self.edl_view = EdlEditor()
        self.controller.set_up_edl_view()
        
        # Set Layout
        input_vbox = QtWidgets.QVBoxLayout()
        tools_vbox = QtWidgets.QVBoxLayout()
        output_vbox = QtWidgets.QVBoxLayout()
        
        input_vbox.addLayout(self.input_layout_left)
        tools_vbox.addLayout(self.tools_layout_left)
        output_vbox.addLayout(self.output_layout_left)
        
        self.input_group_box.setLayout(input_vbox)
        self.tools_group_box.setLayout(tools_vbox)
        self.output_group_box.setLayout(output_vbox)

        self.layout_left.addWidget(self.input_group_box)
        self.layout_left.addWidget(self.tools_group_box)
        self.layout_left.addWidget(self.output_group_box)
        self.layout_right.addWidget(self.edl_view)
        
        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)
        self.setLayout(self.layout)
        
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
