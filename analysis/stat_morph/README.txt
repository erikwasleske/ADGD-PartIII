
Active Dwarf Galaxy Database Part III
/Analysis
	stat_morph
#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
 ** Generates single Service models for galaxies!


** Made statmorph environment:
	(Bash commands)
	$ source .statmorph/bin/activate
	$ pip install WHATEVER IS NEEDE
	$ deactivate

#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%#%
HOW TO:

Just Run run_statmorph.py!
	-> Input file ends up being the parameter file for the Object and Filter stored in /Users/erikjwasleske/Research/ADGD-PartIII/analysis/galfit/paramter_files/OBJID/...

	-> outputs are ./output/convolved_cutout_OBJID_FILTER.png 
			-> Convolved image and pdf cutout used for statmorph fitting
		&
		      ./output/statmorph_OBJID_FILTER.png 
			-> Full 6-panel output of statmorph for Object