"""Parse EDL."""

# Import built-in modules
import os
import re

# Import third-party modules
from edl import Event
from edl import Parser
from timecode import Timecode

# Import local modules
from py_edl_editor.cdl import Cdl


def parse_edl(edl_path, fps):
    """Parse EDL and return list  with EDL Events.

    Args:
        edl_path (str): Absoulte path to EDL.
        fps (float): Frame Rate for EDL calculations.

    Returns:
        Edl: EDL instance.

    """
    parser = Parser(fps)
    if os.path.isfile(edl_path):
        with open(edl_path) as edl_file:
            edl = parser.parse(edl_file)
            for event in edl.events:
                event.cdl = Cdl(event)
                if event.comments:
                    for comment in event.comments:
                        if "ASC_SOP" in comment:
                            event.cdl.set_sop(get_sop(comment))
                        if "ASC_SAT" in comment:
                            event.cdl.set_sat(get_sat(comment))
    return edl


def get_sop(comment):
    """Return dictionary containing all SOP values.

    Args:
        comment (str): EDL Event comment containing the SOP values.

    Returns:
        dict: Dictionary containing all SOP values.

    """
    # https://regex101.com/r/3F8NQd/1
    sop_filter = (
        r"[*]\s?ASC_SOP\s?[(]\s?"
        r"(?P<slope_red>[-]?\d+([.]\d+)?)\s+"
        r"(?P<slope_green>[-]?\d+([.]\d+)?)\s+"
        r"(?P<slope_blue>[-]?\d+([.]\d+)?)\s?[)]\s?[(]\s?"
        r"(?P<offset_red>[-]?\d+([.]\d+)?)\s+"
        r"(?P<offset_green>[-]?\d+([.]\d+)?)\s+"
        r"(?P<offset_blue>[-]?\d+([.]\d+)?)\s?[)]\s?[(]\s?"
        r"(?P<power_red>[-]?\d+([.]\d+)?)\s+"
        r"(?P<power_green>[-]?\d+([.]\d+)?)\s+"
        r"(?P<power_blue>[-]?\d+([.]\d+)?)\s?[)]\s?"
    )
    return re.search(sop_filter, comment).groupdict()
    

def get_sat(comment):
    """Return dictionary containing the SAT value.

    Args:
        comment (str): EDL Event comment containing the SAT value.

    Returns:
        dict: Dictionary containing the SAT value.

    """
    sat_filter = r"[*]\s?ASC_SAT\s?\s?(?P<saturation>[-]?\d+([.]\d+)?)"
    return re.search(sat_filter, comment).groupdict()
