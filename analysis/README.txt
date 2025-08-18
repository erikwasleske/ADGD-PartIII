
Active Dwarf Galaxy Database Part III
/Analysis
#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%

Status / Goals:
	Aug. 18th, 2025
	I have not ran anything for this project in a few months. I believe statmorph was functioning fairly well for some example objects.
	The Goal was to use stat_morph as a quick way to establish an informed prior to using Galfit. 
	Then analyze morphology of dwarf AGN in connection to their selection techniques from ADGD Part I, Wasleske+24.

Ideas:
	Search for a made 'wrapper' for Galfit once get objects working with it. 
	maybe AFFOGATO? See Section 3 of : https://arxiv.org/pdf/2505.10805 of look for different ones!




#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%

Files:

/stat_morph/...
	-> check /stat_morph/README!
	-> tutorial_statmorph.py is just that! Give it a try!
	->run_statmorph.py runs statmorph package on parameter files stored in 
		/analysis/paramter_files/ObjID/...
			-> this files are formatted like GalFit Parameter Files

/isophote_fit/...
	- NOT IN USE
	-> this contains files that have functions to do morphological things
		- ie fit an ellipse to imaging


/galfit/....
	-> so galfit has yet to run for me except for NSA19138_v0
		- which needs to be rerun
		- Read this: https://users.obs.carnegiescience.edu/peng/work/galfit/README.pdf
			- galfit User manual




#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
Journal:

May, 7th, 2025:
	- created ../galfit
		-> directory for gal fit analysis

May 8th, 2025:
	- created ../isophote_fit
		-> contains /ellipse_general.py and /ellispe.py from Prof B. 
			for fitting of ellipse of equal brightness for comparison to brightness profiles

May, 14th, 2025:
	- created ../stat_morph

Aug. 18th, 2025:
	- updating documentation
