"""Models for the QT Table View."""

# Import third-party modules
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class EditableDelegate(QtWidgets.QItemDelegate):
    """Delegate class that enables the cell to be editable."""

    # pylint: disable=invalid-name,no-self-use,too-few-public-methods
    def setEditorData(self, editor, index):
        """Set index to the correct initial value.

        Args:
            editor (QtWidgets.QtWidget): Base class of all user interface
                objects.
            index (QtCore.QModelIndex): Used to locate data in a data model.

        """
        text = index.data(QtCore.Qt.EditRole) or index.data(
            QtCore.Qt.DisplayRole
        )  # noqa: E501
        editor.setText(text)


# pylint: disable=too-few-public-methods
class EdlTableEvent:
    """Main class for EDL Table Event."""

    def __init__(self, edl_event):
        """Initialize the EDL Table Event instance.

        Args:
            edl_event (overcut_exporter.input.edl_event.EdlEvent'): EdlEvent
                instance containing necessary params.

        """
        self.edl_event = edl_event


class EdlTable(QtCore.QAbstractTableModel):
    """QT table showing EDL Events with info and version dropdowns."""

    column_names = [
        "Event#",
        "Reel",
        "Clip Name",
        "Source File",
        "CDL",
        "Locator",
        "Source TC In\nSource TC Out",
        "Rec TC In\nRec TC Out",
        "Source\nDuration",
        "Rec\nDuration",
        "",
    ]

    # pylint: disable=super-with-arguments
    def __init__(self):
        """Initialize the EdlTable instance."""
        super(EdlTable, self).__init__()
        self.events = []
        self.show_frames = False

    def clear(self):
        """Clear the table."""
        self.beginResetModel()
        self.events = []
        self.endResetModel()

    # pylint: disable=invalid-name,unused-argument
    def rowCount(self, index=QtCore.QModelIndex()):
        """Return the tables number of rows.

        Args:
            index (QtCore.QModelIndex): Used to locate data in a data model.

        Returns:
            int: The tables number of rows.

        """
        return len(self.events)

    # pylint: disable=invalid-name,unused-argument
    def columnCount(self, index=QtCore.QModelIndex()):
        """Return the table number of columns.

        Args:
            index (QtCore.QModelIndex): Used to locate data in a data model.

        Returns:
            int: The tables number of columns.

        """
        return len(self.column_names)

    # pylint: disable=invalid-name,unused-argument
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set up header row.

        Args:
            section (int): Number of the given header section.
            orientation (QtCore.Orientation): The objects Orientation.
            role (int): QtCore Role.

        Returns:
            QtCore.QAbstractTableModel.headerData: Table header data.

        """
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return EdlTable.column_names[section]
        return QtCore.QAbstractTableModel.headerData(
            self, section, orientation, role
        )  # noqa: E501

    # pylint: disable=inconsistent-return-statements
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Return data stored under the given role at the given index.

        Args:
            index (QtCore.QModelIndex): Used to locate data in a data model.
            role (int): QtCore Role.

        Returns:
            Data stored under the given role at the given index.


        """
        if role == QtCore.Qt.DisplayRole:
            return self._return_items_role_data(index)

        if role == QtCore.Qt.FontRole and index.column() in [4, 5]:
            return QtGui.QFont("Courier", 10)

        if role == QtCore.Qt.FontRole and index.column() in [6, 7, 8, 9]:
            return QtGui.QFont("Courier", 12)

    # pylint: disable=invalid-name,unused-argument
    def setData(self, index, value, role):
        """Set the role data for the item at index to value.

        Args:
            index (QtCore.QModelIndex): Used to locate data in a data model.
            value (string): Cell value.
            role (int): QtCore Role.

        """
        if index.column() == 1:
            self.events[index.row()].reel = value
        if index.column() == 2:
            self.events[index.row()].clip_name = value
        return True

    # pylint: disable=no-self-use
    def flags(self, index):
        """Return the item flags for the given index.

        Args:
            index (QtCore.QModelIndex): Used to locate data in a data model.

        Returns:
            PySide.QtCore.Qt.ItemFlags: Item flags for the given index.

        """
        if index.column() == 1 or index.column() == 2:
            return (
                QtCore.Qt.ItemIsEditable
                | QtCore.Qt.ItemIsEnabled
                | QtCore.Qt.ItemIsSelectable
            )
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def add_edl_table_event(self, event):
        """Add a row to the table.

        Args:
            event (py_edl_editor.edl_table.EdlTableEvent): Table event that
                will be added to the table.

        """
        self.beginInsertRows(
            QtCore.QModelIndex(), self.rowCount(), self.rowCount()
        )  # noqa: E501
        self.events.append(event)
        self.endInsertRows()

    def edl_events(self):
        """Return a list with the tables EDL Events.

        Returns:
            :obj:'list' of :obj:'overcut_exporter.input.edl_event.EdlEvent':
                List of the tables EdlEvent objects.

        """
        return [event.edl_event for event in self.events]

    # pylint: disable=too-many-return-statements
    def _return_items_role_data(self, index):
        """Return table data for items role.

        Args:
            index (PySide.QtCore.QModelIndex): Qt QModel index instance.

        """
        col = index.column()
        edl_event = self.events[index.row()]
        if col == 0:
            return edl_event.num
        if col == 1:
            return edl_event.reel
        if col == 2:
            return edl_event.clip_name
        if col == 3:
            return edl_event.source_file
        if col == 4:
            return self._cdl_string(edl_event.cdl)
        if col == 5:
            return self._locator_string(edl_event)
        if col == 6:
            src_start = self._timecode_string(edl_event.src_start_tc)
            src_end = self._timecode_string(edl_event.src_end_tc)
            return "{0}\n{1}".format(src_start, src_end)
        if col == 7:
            rec_start = self._timecode_string(edl_event.rec_start_tc)
            rec_end = self._timecode_string(edl_event.rec_end_tc)
            return "{0}\n{1}".format(rec_start, rec_end)
        if col == 8:
            return (edl_event.src_end_tc - edl_event.src_start_tc).frames
        if col == 9:
            return (edl_event.rec_end_tc - edl_event.rec_start_tc).frames

    def _cdl_string(self, cdl):
        """Return a human readable CDL string.

        Args:
            cdl (cdl_convert.Correction): CDL instance.

        Returns:
            string: Human readable CDL string.

        """
        if cdl.has_sat and cdl.has_sop:
            slope = " ".join([str(slope) for slope in cdl.slope])
            offset = " ".join([str(offset) for offset in cdl.offset])
            power = " ".join([str(power) for power in cdl.power])
            return "{0}\n{1}\n{2}\n{3}".format(slope, offset, power, cdl.sat)
        return "-"

    def _locator_string(self, event):
        """Return a human readable Avid Lcator string.

        Args:
            edl_event (Edl.event): EDL Event containing the locator values.

        Returns:
            string: Human readable Avid Locator string.

        """
        if event.has_locator:
            return "{0}\n{1}\n{2}".format(
                event.loc_tc, event.loc_color, event.loc_name
            )  # noqa: E501
        return "-"

    def _timecode_string(self, timecode):
        """Return String representation of the given Timecode instance.

        Depending on show_frames, returning as Frames or SPMTE Timecode String.

        Args:
            timecode (Timecode): Timecode instance to be converted to a string.

        Returns:
            string: String representation of the given Timecode instance either
                as Frames or as SPMTE Timecode String.

        """
        if self.show_frames:
            return str(timecode.frame_number)
        return str(timecode)
