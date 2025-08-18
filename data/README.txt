
Active Dwarf Galaxy Database Part III
/Data
#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
Files:

ADGD_v0_0_9.fits:
	- main data table for 702 bona fide AGN from Wasleske & Baldassare 2024
	- contains all photometry, spectrum values from Part I and SED fit values from Part II
	- Includes separate boolean columns for selections ('BPT' '[OI]-Seyfert', etc. with  =1 selected as AGN, =0 not selected)

ADGD_v0_0_9_obj_pos_HSC_output.csv:
	- output from Hubble Source Catalog Search (4/29/2025)

/Hubble Data Archive Search/ADGD_obj_HST_Archive_obs_totals.fits
	- output from /Hubble Data Archive Search/data_per_object.py (4/30/2025)
	- contains ID, positon, AGN section boolean columns 
		and Columns that are integer sums of Observations from the archive that are 
			- each the HST Instruments (WFPC, WFPC2, WFC3, ASC)
			- each 'W' Wide Filter within those instruments
			- sum of Observation in non-wide filters

/object_data/######
	- contains Hubble Space Telescope (HST) imaging data files


#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
Journal:

April 29th, 2025:
	- Wrote ADGD_v0_0_9.fits
		-> modified from data frame of compile_tSNE_input_table() in
			/Users/erikjwasleske/Research/ADGD-PartII/analysis/functions/compile_selection_tables.py

	- Made ADGD_v0_0_9_obj_pos.csv from [ID, RA, DEC] on TopCat from ADGD_v0_0_0.fits
		-> Input for HST Image search

	- /Hubble Source Catalog Search
		-> pre-finding Wide filter Images, quick Catalog match to see what's there
		https://catalogs.mast.stsci.edu/hsc/
		-> Settings:
			Crossmatch a List of Targets : ADGD_v0_0_9_obj_pos.csv 
			Search Radius: 3 ArcSec 
			Release: v3 | Catalog: Summary | Magnitude Type: MagAper2

		https://catalogs.mast.stsci.edu/hsc/summary-fields.html -> Documentation for Output

		325 targets from ADGD_v0_0_9_obj_pos.csv
		-> made: ADGD_v0_0_9_obj_pos_HSC_output.csv
			-> Only has 227 entire though?

	- /Hubble Data Archive Search
		https://mast.stsci.edu/search/ui/#/hst
		ADGD_v0_0_9_obj_pos_set1.csv  & ADGD_v0_0_9_obj_pos_set2.csv 
			-> Search caps out at 500 objects
		-> Settings:
			3 arminute search
			Data Types = Image | Active Instruments = ACS, WFC3
			Observations = Science | Legacy Instruments = WFPC1 , WFPC2
		(see HST_Image_Query for Show API Query copy produced with these settings)
		-> Resulting:
			HST_query_set1.csv  &  HST_query_set2.csv

April 30th, 2025:
	- /Hubble Data Archive Search
		-> created /data_per_object.py
			- connect outputs of Archive Search to galaxies in ADGD
			- created /ADGD_obj_HST_Archive_obs_totals.fits
			- 16 entries from Archive did not get added to this table!!!!

May 7th, 2025:
	- /Hubble Data Archive Search
		-> edited /data_per_object.py to settle issues
		-> /ADGD_obj_HST_Archive_obs_totals.fits should now be accurate W filter data availability table
			-> with caveat of 16 entries match NO galaxy 
		
	- made /object_data
		-> directory will hold folders named after object ID that contain the image files

May 8th, 2025:
	- working on NSA104527_v0
		- data is in /object_data/NAS104527_v0

Aug. 18th, 2025:
	- updating this documentation
		

			
			
		
