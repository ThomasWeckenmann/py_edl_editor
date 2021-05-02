"""Tests for TC Tools."""

# Import built-in modules
import os

# Import local modules
from py_edl_editor.edl_parser import parse_edl
from py_edl_editor.edl_parser import remove_edl_gaps


def test_remove_tc_gaps():
    dirname = os.path.dirname(__file__)
    edl_with_gaps_path = os.path.join(dirname, "files/edl_with_gaps.edl")
    edl_without_gaps_path = os.path.join(dirname, "files/edl_without_gaps.edl")
    gap_edl = parse_edl(edl_with_gaps_path, "24")
    no_gap_edl = parse_edl(edl_without_gaps_path, "24")
    assert no_gap_edl.to_string() == remove_edl_gaps(gap_edl).to_string()