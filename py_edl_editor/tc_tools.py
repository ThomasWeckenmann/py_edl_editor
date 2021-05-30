"""Timecode tools."""

# Import third-party modules
from timecode import Timecode  # type: ignore


def remove_edl_gaps(edl):
    """Return EDL without gaps between EDL Events.

    Args:
        edl (Edl): Edit Decision List.

    Return:
        Edl: Edit Decision List without gaps.

    """
    for index in range(len(edl.events) - 1):
        event_rec_end = edl.events[index].rec_end_tc
        next_event_rec_start = edl.events[index + 1].rec_start_tc
        next_event_rec_end = edl.events[index + 1].rec_end_tc
        diff = next_event_rec_start.frames - event_rec_end.frames
        if diff > 0:
            tc_diff = next_event_rec_start - event_rec_end
            edl.events[index + 1].rec_start_tc = next_event_rec_start - tc_diff
            edl.events[index + 1].rec_end_tc = next_event_rec_end - tc_diff
        # Special case: EDL with incorrect order:
        if diff < 0:
            tc_diff = event_rec_end - next_event_rec_start
            edl.events[index + 1].rec_start_tc = next_event_rec_start + tc_diff
            edl.events[index + 1].rec_end_tc = next_event_rec_end + tc_diff
    return edl


def set_edl_start_tc(edl, start_tc):
    """Return EDL with updated start timecode.

    Args:
        edl (Edl): Edit Decision List.
        start_tc (string): String representing the start of the new EDL.

    Return:
        Edl: Edit Decision List with updated start timecode.

    """
    new_start_tc = tc_from_string(edl.fps, start_tc)
    if new_start_tc:
        first_event_rec_start = edl.events[0].rec_start_tc
        diff = edl.events[0].rec_start_tc - new_start_tc
        for event in edl.events:
            if first_event_rec_start > new_start_tc:
                event.rec_start_tc = event.rec_start_tc - diff
                event.rec_end_tc = event.rec_end_tc - diff
            else:
                event.rec_start_tc = event.rec_start_tc + diff
                event.rec_end_tc = event.rec_end_tc + diff
    return edl


def tc_from_string(framerate, start_tc):
    """Convert and return string to Timecode instance.

    String can be either a frame number or a string in smpte timecode format
    like: "hh:mm:ss:ff".

    Args:
        framerate (string): Framerate to calculate the Timecode instance.
        start_tc (string): String to be converted to a Timecode instance.

    Return:
        Timecode: Timecode instance calculated from input string.

    """
    new_start_tc = None
    try:
        frames = int(start_tc)
        new_start_tc = Timecode(framerate, "00:00:00:{0}".format(frames))
    except ValueError:
        try:
            new_start_tc = Timecode(framerate, start_tc)
        except (IndexError, ValueError):
            print("Wrong Timcode format: {0}".format(start_tc))
    return new_start_tc


def add_handles_to_edl(edl, handles):
    """Return EDL with added handles.

    Args:
        edl (Edl): Edit Decision List.
        handles (int): Number of handles to be added to each event.

    Return:
        Edl: Edit Decision List with added handles.
    """
    first_event_rec_start = edl.events[0].rec_start_tc
    if (first_event_rec_start.frame_number - handles) < 0:
        edl = set_edl_start_tc(edl, str((first_event_rec_start + handles)))
    for event in edl.events:
        event.src_start_tc = event.src_start_tc - handles
        event.src_end_tc = event.src_end_tc + handles
        event.rec_start_tc = event.rec_start_tc - handles
        event.rec_end_tc = event.rec_end_tc + handles
    return edl
