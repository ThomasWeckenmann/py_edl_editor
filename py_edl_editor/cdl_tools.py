"CDL tools."

# Import third-party modules
import cdl_convert  # type: ignore


def add_ccc_to_edl(edl, ccc_file_path):
    """Add cdl values of the .ccc file to the EDL.

    Args:
        edl (Edl): Edit Decision List.
        ccc_file_path (string): Absolute pth to the .ccc file.

    """
    # Clear members, so the ids are empty and no unique ids are created.
    cdl_convert.correction.ColorCorrection.members = {}
    ccc = cdl_convert.parse_ccc(ccc_file_path)
    _import_cdls(edl, ccc.color_corrections)


def add_cdls_to_edl(edl, cdl_type, cdl_file_paths):
    """Add cdl values of the .cc or .cdl files to the EDL.

    Args:
        edl (Edl): Edit Decision List.
        cdl_type (string): Type of CDL (.cc, .cdl).
        cdl_file_paths (list): List of paths to the .cdl/.cc files.

    """
    cdls = []
    cdl_convert.correction.ColorCorrection.members = {}
    for path in cdl_file_paths:
        if cdl_type == ".cdl":
            decisions = cdl_convert.parse_cdl(path).color_decisions
            for decision in decisions:
                cdls.append(decision.cc)
        if cdl_type == ".cc":
            cdls.append(cdl_convert.parse_cc(path))
    _import_cdls(edl, cdls)


def _import_cdls(edl, cdls):
    """Add cdl values of the collection to the EDL.

    Args:
        edl (Edl): Edit Decision List.
        ccc_file_path (string): Absolute pth to the .ccc file.

    """
    for cdl in cdls:
        for event in edl.events:
            if event.reel == cdl.id:
                event.cdl = cdl
                _add_edl_cdl_comments(event)


def _add_edl_cdl_comments(event):
    """Add CDL comments to the edl event.

    Args:
        event (Edl.event): EDL Event where CDL comments will be added.

    """
    _remove_edl_cdl_comments(event)
    slope = " ".join([str(slope) for slope in event.cdl.slope])
    offset = " ".join([str(offset) for offset in event.cdl.offset])
    power = " ".join([str(power) for power in event.cdl.power])
    sop = "* ASC_SOP ({0})({1})({2})".format(slope, offset, power)
    sat = "* ASC_SAT {0}".format(event.cdl.sat)
    event.comments.append(sop)
    event.comments.append(sat)


def _remove_edl_cdl_comments(event):
    """Remove all CDL comments from the edl event.

    Args:
        event (Edl.event): EDL Event containing the comments to remove.

    """
    cdl_comments = []
    for comment in event.comments:
        if "ASC_SOP" in comment:
            cdl_comments.append(comment)
        elif "ASC_SAT" in comment:
            cdl_comments.append(comment)
    if cdl_comments:
        for comment in cdl_comments:
            event.comments.remove(comment)
