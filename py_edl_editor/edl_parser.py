"""EDL parser."""

# Import built-in modules
import os
import re

# Import third-party modules
from edl import Parser
from cdl_convert import correction


def parse_edl(edl_path, fps):
    """Parse EDL and return list  with EDL Events.

    Args:
        edl_path (str): Absoulte path to EDL.
        fps (float): Frame Rate for EDL calculations.

    Returns:
        Edl: EDL instance.

    """
    edl = None
    parser = Parser(fps)
    # Clear members, so the ids are empty and no unique ids are created.
    correction.ColorCorrection.members = {}
    if os.path.isfile(edl_path):
        with open(edl_path) as edl_file:
            edl = parser.parse(edl_file)
            for i, event in enumerate(edl.events):
                event.cdl = correction.ColorCorrection(event.reel)
                if event.comments:
                    for comment in event.comments:
                        if "ASC_SOP" in comment:
                            event.cdl = add_sop(event.cdl, comment)
                        if "ASC_SAT" in comment:
                            event.cdl.sat = get_sat(comment)
    return edl


def add_sop(cdl, comment):
    """Return cdl with added SOP values.

    Args:
        cdl (cdl_convert.Correction): Correction instance (Color Decision List).
        comment (str): EDL Event comment containing the SOP values.

    Returns:
        Correction: cdl_convert Correction instance with added SOP values.

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
    sop = re.search(sop_filter, comment).groupdict()
    cdl.slope = (sop["slope_red"], sop["slope_green"], sop["slope_blue"])
    cdl.offset = (sop["offset_red"], sop["offset_green"], sop["offset_blue"])
    cdl.power = (sop["power_red"], sop["power_green"], sop["power_blue"])
    return cdl
    

def get_sat(comment):
    """Return the events SAT value.

    Args:
        comment (str): EDL Event comment containing the SAT value.

    Returns:
        string: SAT value.

    """
    sat_filter = r"[*]\s?ASC_SAT\s?\s?(?P<saturation>[-]?\d+([.]\d+)?)"
    return re.search(sat_filter, comment).groupdict()["saturation"]
