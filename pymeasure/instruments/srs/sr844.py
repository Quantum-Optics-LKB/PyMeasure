

import re
import time
import numpy as np
from enum import IntFlag
from pymeasure.instruments import Instrument, discreteTruncate
from pymeasure.instruments.validators import strict_discrete_set, \
    truncated_discrete_set, truncated_range
from sr830 import SR830


class LIAStatus(IntFlag):
    """ IntFlag type that is returned by the lia_status property.
    """
    REF_UNLOCK = 0                  #Reference unlock
    REF_FREQ_OUT_OF_RANGE = 1       #Reference frequency out of range
    
    TRIGGER = 3                     #Data storage triggered
    SIGNAL_INPUT_OVERLOADS = 4      #Signal input overload
    IF_AMPLIFIER_OVERLOADS = 5      #IF amplifier overload
    FLT_OUT_OF_RANGE = 6            #Filter out of range

    FREQ_CHG = 7                    #Ref frequency changed by more than 1% 
    CH1 = 8                         #CH1 display OL
    CH2 = 9                         #CH2 display OL


class SR844(SR830):


    def get_scaling(self):

        """ Returns both the offset and expand scaling factors on the 'R' measurement
        """
        offset = self.ask('DOFF?1,1' )  
        expand = self.ask('DEXP?1,1')
        return float(offset), float(expand)

    def is_sensitivity_out_of_range(self):
        
        """ Returns True if the filter is out of range
        """
        return int(self.ask("LIAS?5")) == 1
        