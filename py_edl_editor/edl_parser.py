"""EDL parser."""

# Import built-in modules
import os
import re

# Import third-party modules
from edl import Parser  # type: ignore
from cdl_convert import correction  # type: ignore


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
            for event in edl.events:
                event.cdl = correction.ColorCorrection(event.reel)
                event.has_locator = False
                if event.comments:
                    for comment in event.comments:
                        if "ASC_SOP" in comment:
                            add_sop(event.cdl, comment)
                        if "ASC_SAT" in comment:
                            add_sat(event.cdl, comment)
                        if "LOC: " in comment:
                            add_avid_locator(event, comment)
    return edl


def add_sop(cdl, comment):
    """Add SOP values to the cdl instance.

    Args:
        cdl (cdl_convert.Correction): Correction instance.
        comment (str): EDL Event comment containing the SOP values.

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


def add_sat(cdl, comment):
    """Add SAT values to the cdl instance.

    Args:
        cdl (cdl_convert.Correction): Correction instance.
        comment (str): EDL Event comment containing the SAT value.

    """
    sat_filter = r"[*]\s?ASC_SAT\s?\s?(?P<saturation>[-]?\d+([.]\d+)?)"
    cdl.sat = re.search(sat_filter, comment).groupdict()["saturation"]


def add_avid_locator(event, comment):
    """Add Avid Locator values to the event.

    Args:
        event (Edl.event): Event instance to which locator info will be added.
        comment (str): EDL Event comment containing the Avid Locator values.

    """
    # https://regex101.com/r/b8QOPl/1
    loc_filter = (
        r"[*]\s?LOC:\s+?"
        r"(?P<timecode>\d{2}[:]\d{2}[:]\d{2}[:]\d{2})\s+"
        r"(?P<color>[\S+]*)\s+"
        r"(?P<name>.*)"
    )
    try:
        locator_dict = re.search(loc_filter, comment).groupdict()
        event.loc_tc = locator_dict["timecode"]
        event.loc_color = locator_dict["color"]
        event.loc_name = locator_dict["name"]
        event.has_locator = True
    except AttributeError:
        pass
