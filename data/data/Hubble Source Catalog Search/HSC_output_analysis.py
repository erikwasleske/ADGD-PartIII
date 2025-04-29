from astropy.io import ascii
import astropy.units as u
from astropy.table import Table, join
import numpy as np
"""""
Deducing Hubble Source Catalog (HSC) output file
../ADGD-PartIII/data/ADGD_v0_0_9_obj_pos_HSC_output.csv
    - Multiple entries in this file per position
    - Want to connect single master HSC entry to objects in ADGD 
"""""
search_result = ascii.read('/Users/erikjwasleske/Research/ADGD-PartIII/data/ADGD_v0_0_9_obj_pos_HSC_output.csv')


