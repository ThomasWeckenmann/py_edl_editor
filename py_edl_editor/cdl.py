"CDL class containing all needed CDL values."

class Cdl(object):
    """Main class for Cdl."""
    
    def __init__(self, event):
        """Initialize cdl class.

        Args:
            event (Edl.event): EDL event instance.

        """
        self.event = event
        self._is_empty = True
        
        self.saturation = 1.0
        
        self.slope_red = 1.0
        self.slope_green = 1.0
        self.slope_blue = 1.0
        self.offset_red = 0.0
        self.offset_green = 0.0
        self.offset_blue = 0.0
        self.power_red = 1.0
        self.power_green = 1.0
        self.power_blue = 1.0
    
    def set_sop(self, asc_sop):
        """Set SOP values.
        
        Args:
            asc_sop (dict): Dictionary containing all SOP values.
        
        """
        self.slope_red = asc_sop["slope_red"]
        self.slope_green = asc_sop["slope_green"]
        self.slope_blue = asc_sop["slope_blue"]
        
        self.offset_red = asc_sop["offset_red"]
        self.offset_green = asc_sop["offset_green"]
        self.offset_blue = asc_sop["offset_blue"]
        
        self.power_red = asc_sop["power_red"]
        self.power_green = asc_sop["power_green"]
        self.power_blue = asc_sop["power_blue"]
        
        self._is_empty = False
    
    def set_sat(self, asc_sat):
        """Set SAT value.
        
        Args:
            asc_sat (dict): Dictionary containing the SAT value.
        
        """
        self.saturation = asc_sat["saturation"]
        self._is_empty = False
        
    def cc_xml(self):
        """Return CDL in the ColorCorrection (.cc) format.
        
        Returns:
            list: List containing all lines of the ColorCorrection XML.
        
        """
        lines = []
        lines.append(f"<ColorCorrection id='{self.event.reel}'>")
        lines.append(f"\t<SOPNode>")
        lines.append(f"\t\t<Slope>{self.slope_red} {self.slope_green} {self.slope_blue}</Slope>")
        lines.append(f"\t\t<Offset>{self.offset_red} {self.offset_green} {self.offset_blue}</Offset>")
        lines.append(f"\t\t<Power>{self.power_red} {self.power_green} {self.power_blue}</Power>")
        lines.append(f"\t</SOPNode>")
        lines.append(f"\t<SatNode>")
        lines.append(f"\t\t<Saturation>{self.saturation}</Saturation>")
        lines.append(f"\t</SatNode>")
        lines.append("</ColorCorrection>") 
        return lines
    
    def cdl_xml(self):
        """Return CDL in the ColorCorrection (.cc) format.
        
        Returns:
            list: List containing all lines of the ColorCorrection XML.
        
        """
        lines = []
        lines.append("<?xml version='1.0' encoding='UTF-8'?>")
        lines.append("<ColorDecisionList xmlns='urn:ASC:CDL:v1.01'>")
        lines += self._tabbed_cc_xml()
        lines.append("</ColorDecisionList>")
        return lines
    
    def _tabbed_cc_xml(self):        
        """Return CDL in the ColorCorrection (.cc) format.
        
        Each line prependended by a tab.
        
        Returns:
            list: List containing all lines of the ColorCorrection XML.
        
        """
        return [f"\t{line}" for line in self.cc_xml()]
    
    def __str__(self):
        """Return a string representation of the CDL instance."""
        if self._is_empty:
            return "-"
        return (f"{self.slope_red} {self.slope_green} {self.slope_blue}\n"
                f"{self.offset_red} {self.offset_green} {self.offset_blue}\n"
                f"{self.power_red} {self.power_green} {self.power_blue}\n"
                f"{self.saturation}")

def ccc_xml(cdls):
    """Return CDL in the ColorCorrectionCollection (.ccc) format.
    
    Returns:
        list: List containing all lines of the ColorCorrectionCollection XML.
    
    """
    lines = []
    lines.append("<?xml version='1.0' encoding='UTF-8'?>")
    lines.append("<ColorCorrectionCollection xmlns='urn:ASC:CDL:v1.01'>")
    for cdl in cdls:
        lines += cdl._tabbed_cc_xml()
    lines.append("</ColorCorrectionCollection>")
    return lines
