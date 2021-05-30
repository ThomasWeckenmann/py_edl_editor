"""Tests for timecode tools."""

# Import built-in modules
import os

# Import third-party modules
from timecode import Timecode  # type: ignore

# Import local modules
from py_edl_editor.edl_parser import parse_edl
from py_edl_editor.tc_tools import add_handles_to_edl
from py_edl_editor.tc_tools import remove_edl_gaps
from py_edl_editor.tc_tools import set_edl_start_tc
from py_edl_editor.tc_tools import tc_from_string

DIRNAME = os.path.dirname(__file__)


def test_remove_tc_gaps():
    """Returns correctly calculated EDL without gaps."""
    edl_with_gaps_path = os.path.join(DIRNAME, "files/edl_with_gaps.edl")
    edl_without_gaps_path = os.path.join(DIRNAME, "files/edl_without_gaps.edl")
    gap_edl = parse_edl(edl_with_gaps_path, "24")
    no_gap_edl = parse_edl(edl_without_gaps_path, "24")
    assert no_gap_edl.to_string() == remove_edl_gaps(gap_edl).to_string()


def test_set_start_tc():
    """Returns correctly calculated EDL with updated start tc."""
    edl_with_gaps_path = os.path.join(DIRNAME, "files/edl_with_gaps.edl")
    zero_start_path = os.path.join(DIRNAME, "files/edl_with_gaps_start0.edl")
    test_edl = parse_edl(edl_with_gaps_path, "24")
    zero_start_edl = parse_edl(zero_start_path, "24")
    expected = set_edl_start_tc(test_edl, "0").to_string()
    assert zero_start_edl.to_string() == expected


def test_tc_from_string_with_frame_input():
    """Returns correct tc instance from string containing a frame number."""
    input_frames = "86400"
    expected = Timecode("24", "01:00:00:00")
    assert tc_from_string("24", input_frames) == expected


def test_tc_from_string_with_smpte_input():
    """Returns correct tc instance from string containing a smpte tc string."""
    input_tc = "00:00:00:10"
    expected = Timecode("24", "00:00:00:10")
    assert tc_from_string("24", input_tc) == expected


def test_add_handles_to_edl():
    """Returns correctly calculated EDL with added handles."""
    gaps_edl = os.path.join(DIRNAME, "files/edl_with_gaps_start0.edl")
    handles_edl_path = "files/edl_with_gaps_start0_plus_handles.edl"
    handles_edl = os.path.join(DIRNAME, handles_edl_path)
    test_edl = parse_edl(gaps_edl, "24")
    handles_edl = parse_edl(handles_edl, "24")
    expected = add_handles_to_edl(test_edl, 8).to_string()
    assert handles_edl.to_string() == expected
