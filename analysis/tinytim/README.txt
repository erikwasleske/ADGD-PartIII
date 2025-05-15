
Active Dwarf Galaxy Database Part III

	tinytim
#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
 ** Generates the PSF model for each HST Filter!

User's Manual: https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/focus-and-pointing/documentation/_documents/tinytim.pdf


#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%

A) Run tinytim for all Filters used
	-> alias and paths in example point to /Users/erikjwasleske/tinytim/tinytim-7.5
	STEPS in RUNNING
	 (I have made a bash source to store all aliases in my base user directory)
	1) 'Open up the terminal'
	2) $ source ~/tinytim_alias
	3) (Decide for what Instruement, example for WFC3)
	4) $ tiny1 wfc3.in
	5) Make choices within tiny1
	6) $ tiny2 wfc3.in
	8) $ tiny3 wfc3.in
 
		
#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
GENEREAL INSTRUMENT PSF SETTING CHOICES:

WFC3:
	(Tiny1)
	-> Choose form of object Spectra: select Blackbody ( 2) ) 
	-> Enter Temperature (Kelvin): 10000
	-> Focus, secondary mirror despace? [microns]: ** See 'HST_despace_measurements.pdf' -Rivera2024
	-> positions set to 500 500 (center of WFC3 ccd)

 !!!!!! In doing TinyTim, the sampling pixel size is NOT an input!
	-> was thought to be a potential issue with the PSFs (May 15th, 2025)

#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%


#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%

CONTENTS OF TINYTIM Aliases BASH SCRIPT:

#!/bin/bash

TINYTIM=/Users/erikjwasleske/tinytim/tinytim-7.5
export TINYTIM
alias tiny1=/Users/erikjwasleske/tinytim/tinytim-7.5/tiny1
alias tiny2=/Users/erikjwasleske/tinytim/tinytim-7.5/tiny2
alias tiny3=/Users/erikjwasleske/tinytim/tinytim-7.5/tiny3
printf " TinyTime Aliases are set. \n"




