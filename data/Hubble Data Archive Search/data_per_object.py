from astropy.io import ascii, fits
import astropy.units as u
from astropy.table import Table, join
import numpy as np
"""""
Deducing Hubble Source Catalog (HSC) output file
../ADGD-PartIII/data/ADGD_v0_0_9_obj_pos_HSC_output.csv
    - Multiple entries in this file per position
    - Want to connect single master HSC entry to objects in ADGD 
"""""
#### LOAD DATABSE & HST ARCHIVE QUERY OUTPUT
print(' Loading ADGD and HST Archive Query Result tables.')
adgd = Table(fits.open('/Users/erikjwasleske/Research/ADGD-PartIII/data/ADGD_v0_0_9.fits')[1].data)
archive_output = ascii.read('/Users/erikjwasleske/Research/ADGD-PartIII/data/Hubble Data Archive Search/HST_query_fullset.csv')
#################################################################
#### FORMAT NEW TABLE FOR RESULTS
print('Creating a Results Table to hold info about Observations of Galaxies from ADGD within HST Archive.')
colnames = ['ID','RA','DEC',
            'BPT','[OI]-Seyfert','[OI]-LINER','[SII]-Seyfert','[SII]-LINER','[HeII]','broad-line','IR','X-ray','Var.',
            'Total_Obs_Num', 'WFPC', 'WFPC2', 'WFC3' , 'ACS',
            'F105W', 'F110W', 'F125W', 'F140W', 'F160W', 'F170W','F218W', 'F255W', 'F275W', 'F284W',
            'F300W', 'F336W', 'F390W', 'F438W', 'F439W', 'F450W', 'F475W','F555W', 'F702W', 'F775W',  'F814W',
            'CLEAR1L;F435W', 'CLEAR1L;F814W', 'CLEAR1S;F330W',
            'F475W;CLEAR2L', 'F555W;CLEAR2L', 'F555W;CLEAR2S', 'F606W', 'F606W;CLEAR2L', 'F625W;CLEAR2S', 'F775W;CLEAR2L', 'F775W;CLEAR2S',
            'Other_Filter'

            #'Instruments', 'Filters'
            ]
dtypes = ['<U23'] + [np.float64] * 2 + [np.bool] * 10 + [np.int64] + [np.int64] * 37
units = [u.dimensionless_unscaled] + [u.degree] * 2 + [u.dimensionless_unscaled] * 48
results_table = Table( names = colnames, dtype = dtypes, units = units) # Defining Results Table

#################################################################
#### Fill Results Table with Observation Details
print('     Filling out... ')
not_matched = 0
for i in range(0, len(archive_output)):
    # Matching Positions in Archive Output of ADGD:
    adgd_obj = adgd[np.round(adgd['RA'], 5) == float(archive_output['search_pos'][i].split(' ')[0])] and \
               adgd[np.round(adgd['DEC'], 5) == float(archive_output['search_pos'][i].split(' ')[1])]
    if len(adgd_obj) == 0:
        print('         !!! Entry in HST Archive is not matching to ADGD Object')
        not_matched +=1
    if len(adgd_obj) == 1:
        # If this Object is not in the Results Table, Add new Row:
        if adgd_obj['ID'][0] not in results_table['ID']:
            results_table.add_row() # Add new row to Results table
            results_table[-1]['ID','RA','DEC', 'BPT','[OI]-Seyfert','[OI]-LINER','[SII]-Seyfert','[SII]-LINER','[HeII]','broad-line','IR','X-ray','Var.']\
                = adgd_obj[0]['ID','RA','DEC', 'BPT','[OI]-Seyfert','[OI]-LINER','[SII]-Seyfert','[SII]-LINER','[HeII]','broad-line','IR','X-ray','Var.']
            results_table[-1][archive_output[i]['sci_instrume']] +=1 # Add +1 to whichever Instrument was used in the Observation
            if archive_output[i]['sci_spec_1234'] in colnames: # If filter name is in column list (colnames)of Wide Filters:
                results_table[-1][archive_output[i]['sci_spec_1234']] +=1 # Add +1 to whichever filter was used in the Observation
            if archive_output[i]['sci_spec_1234'] not in colnames: # If in filter not specificed:
                results_table[-1]['Other_Filter'] += 1 # Add +1 to Other_Filter value



        # If this Object is in the Results Table, Add Instrument and Filter to Row:
        if adgd_obj['ID'][0] in results_table['ID']:
            index = np.where(results_table['ID'] == adgd_obj['ID'])[0][0] # find which index in the Results Table this Object lives
            results_table[index][archive_output[i]['sci_instrume']] +=1 # Add +1 to whichever Instrument was used in the Observation
            if archive_output[i]['sci_spec_1234'] in colnames: # If filter name is in column list (colnames)of Wide Filters:
                results_table[index][archive_output[i]['sci_spec_1234']] +=1 # Add +1 to whichever filter was used in the Observation
            if archive_output[i]['sci_spec_1234'] not in colnames: # If in filter not specificed:
                results_table[index]['Other_Filter'] += 1 # Add +1 to Other_Filter value
print(' Completed filling out Results Table with Objects and their Instrument/Filter Observation Counts in the HST Archive.')
print('Number of entries from HST Archive Query Results that did NOT match an ADGD galaxy: ' , not_matched)

#################################################################
#### Write Results Table to File

writing = str(input('  Save these results to a file? (y/n)'))
path = '/Users/erikjwasleske/Research/ADGD-PartIII/data/Hubble Data Archive Search/' # Target Path for File
if writing =='y': #Wanting to write Database Table to file
    results_table.write( path +'ADGD_obj_HST_Archive_obs_totals' +'.fits'  , format='fits', overwrite=True) # Act of writing to File
    print('Results Table written to:  ', path +'ADGD_obj_HST_Archive_obs_totals' +'.fits')
###################################################################################


#################################################################
#################################################################
#################################################################
#################################################################
#################################################################

#### Scratch Material to help with developing this code:

# List off all Wide ('W) Filters:
#filter_list = []
#for i in range(0, len(archive_output)):
#    if'W' in archive_output['sci_spec_1234'][i]:
#        if archive_output['sci_spec_1234'][i] not in filter_list:
#            filter_list.append(archive_output['sci_spec_1234'][i])
