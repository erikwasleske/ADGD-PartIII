import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.visualization import simple_norm
from astropy.modeling.models import Sersic2D
from astropy.convolution import convolve, Gaussian2DKernel
from photutils.segmentation import detect_threshold, detect_sources
from photutils.background import Background2D, MedianBackground

import time
import statmorph
from statmorph.utils.image_diagnostics import make_figure
#matplotlib inline
#################################################################
"""""
Using the statmorph package to quickly get properties of the morphology
"""""
#################################################################
### LOAD IN DATA:

obj_name = input(print('Object name: '))
filter_name = input(print('Filter name: '))
    #Ex:
#obj_name = 'NSA104527_v0'
#filter_name = 'F140W'
#data = fits.open('/Users/erikjwasleske/galfit/data/NSA19138_v0/MAST_2024-09-26T19_03_49.113Z/HST/icuu27010_drz.fits')[1].data


#give an parameter file
input_file = '/Users/erikjwasleske/Research/ADGD-PartIII/analysis/galfit/paramter_files/'+obj_name+'/'+obj_name+'_'+filter_name+'_parms.txt'

with open(input_file, 'r') as fp: #CHANGE NUMBER, WHEN READY FOR NEXT MODEL
    lines = fp.readlines()
data = fits.open(lines[7].split()[1][:-3])[1].data
print('  data file is : ', lines[7].split()[1][:-3])
psf = fits.open(lines[10].split()[1])[0].data
print('  psf file is : ' , lines[10].split()[1])

print('  Importing Image data and generating cutout of galaxy.')
position =( float(lines[40].split()[1]) , float(lines[40].split()[2]))
print(' Position of galaxy in pixel Image units is: ' , position)
#position = (286.6464, 251.7688) # x,y in Image coordinates
size = (200,200)#(90,90)#(410-75 , 435-134) # y, x for cutout!!
    #Ex2:
#obj_name = 'NSA104527_v0'
#filter_name = 'F140W'
#data = fits.open('/Users/erikjwasleske/Research/ADGD-PartIII/data/object_data/NSA104527_v0/HST/F140W/hst_15607_03_wfc3_ir_f140w_idwm03_drz.fits')[1].data
#print('  Importing Image data and generating cutout of galaxy.')
#position = (343.34946, 315.59685) # x,y in Image coordinates
#size = (125,125)#(410-75 , 435-134) # y, x for cutout!!
    #Ex3:
#obj_name = 'NSA104527_v0'
#filter_name = 'F336W'
#data = fits.open('/Users/erikjwasleske/Research/ADGD-PartIII/data/object_data/NSA104527_v0/HST/F336W/hst_15607_03_wfc3_uvis_f336w_idwm03_drc.fits')[1].data
#print('  Importing Image data and generating cutout of galaxy.')
#position = (649.12276, 667.42034) # x,y in Image coordinates
#size = (125,125)#(410-75 , 435-134) # y, x for cutout!!

### MAKE CUTOUT:
cutout = Cutout2D(data, position, size)
plt.imshow(cutout.data, cmap='gray', origin='lower',
           norm=simple_norm(cutout.data, stretch='log', log_a=10000))
print('  Printing cutout')
plt.show(block=True)
#################################################################
### SUBTRACTING BACKGROUND
# Estimate background using photutils
#bkg_estimator = MedianBackground()
#bkg = Background2D(cutout.data, size, filter_size=(3,3), bkg_estimator=bkg_estimator)
#################################################################
### LOAD IN PSF:
    #Ex:
#psf = fits.open('/Users/erikjwasleske/galfit/paramter_files/f110w_blackbody00.fits')[0].data
print(' Create a PSF cutout that is odd size for Kernel size for convolution must be odd in all axes')
if psf.shape[0] % 2 != 0:
    psf = Cutout2D(psf, (psf.shape[0]/2,psf.shape[1]/2), (psf.shape[0],psf.shape[1]))
if psf.shape[0] % 2 == 0 :
    psf = Cutout2D(psf, (psf.shape[0]/2,psf.shape[1]/2), (psf.shape[0]-1,psf.shape[1]-1))

    #Ex2:

    #Ex3:
#psf = fits.open('')[1].data
#psf = Cutout2D(psf, (), ()),



#plt.imshow(psf.data, cmap='gray', origin='lower',
#           norm=simple_norm(psf.data, stretch='log', log_a=10000))
#print('  Printing PSF.')
#plt.show(block=True)

#################################################################
### DEFINE GAIN
print('   defining Gain from Fits Header.')
gain = fits.open(lines[7].split()[1][:-3])[0].header['CCDGAIN']#1e5 #2.5 # From header : CCDGAIN =   2.5 / commanded gain of CCD


#################################################################
### CONVOLVE WITH PSF:
print('  Convolving cutout with PSF')
image = convolve(cutout.data, psf.data)

plt.imshow(image, cmap='gray', origin='lower',
           norm=simple_norm(cutout.data, stretch='log', log_a=10000))
print('  Printing  & saving convolved cutout.')
plt.savefig('output/convolved_cutout_'+obj_name+'_'+filter_name+'.png', dpi=150)

plt.show(block=True)
#################################################################
### CREATING SEGMENTATION MAP
print('  Creating Segmentation Map')
threshold = detect_threshold(image, 5)
npixels = 5  # minimum number of connected pixels
segmap = detect_sources(image, threshold, npixels)
plt.imshow(segmap, origin='lower', cmap='gray')
plt.show(block=True)
print('   Print segmation map')


#################################################################
### RUNNING STATMORPH
print('  Running statmorph')
start = time.time()
source_morphs = statmorph.source_morphology(
    cutout.data, segmap, gain=gain, psf=psf.data)
print('Time: %g s.' % (time.time() - start))
print(' Finding source closest to galaxy  of interest (centered in cutout)')
distance = [np.nan] * len(source_morphs)
for i in range (0 , len(source_morphs)):
    x1, y1 = source_morphs[i]._centroid
    obj_pos_x , obj_pos_y = (size[0]/2 , size[1]/2)
    distance[i] = np.sqrt((obj_pos_x - x1)**2 + (obj_pos_y - y1)**2)
print('  Identified source is ' , np.around(np.nanmin(distance), 2) ,' pixels away for galaxy at center of cutout')
obj_idx = np.where(distance == np.nanmin(distance))[0][0]
morph = source_morphs[obj_idx]

### PRINT MORPHOLOGY PORPERTIES:
print('BASIC MEASUREMENTS (NON-PARAMETRIC)')
print('xc_centroid =', morph.xc_centroid)
print('yc_centroid =', morph.yc_centroid)
print('ellipticity_centroid =', morph.ellipticity_centroid)
print('elongation_centroid =', morph.elongation_centroid)
print('orientation_centroid =', morph.orientation_centroid)
print('xc_asymmetry =', morph.xc_asymmetry)
print('yc_asymmetry =', morph.yc_asymmetry)
print('ellipticity_asymmetry =', morph.ellipticity_asymmetry)
print('elongation_asymmetry =', morph.elongation_asymmetry)
print('orientation_asymmetry =', morph.orientation_asymmetry)
print('rpetro_circ =', morph.rpetro_circ)
print('rpetro_ellip =', morph.rpetro_ellip)
print('rhalf_circ =', morph.rhalf_circ)
print('rhalf_ellip =', morph.rhalf_ellip)
print('r20 =', morph.r20)
print('r80 =', morph.r80)
print('Gini =', morph.gini)
print('M20 =', morph.m20)
print('F(G, M20) =', morph.gini_m20_bulge)
print('S(G, M20) =', morph.gini_m20_merger)
print('sn_per_pixel =', morph.sn_per_pixel)
print('C =', morph.concentration)
print('A =', morph.asymmetry)
print('S =', morph.smoothness)
print()
print('SERSIC MODEL')
print('sersic_amplitude =', morph.sersic_amplitude)
print('sersic_rhalf =', morph.sersic_rhalf)
print('sersic_n =', morph.sersic_n)
print('sersic_xc =', morph.sersic_xc)
print('sersic_yc =', morph.sersic_yc)
print('sersic_ellip =', morph.sersic_ellip)
print('sersic_theta =', morph.sersic_theta)
print('sersic_chi2_dof =', morph.sersic_chi2_dof)
print()
print('OTHER')
print('sky_mean =', morph.sky_mean)
print('sky_median =', morph.sky_median)
print('sky_sigma =', morph.sky_sigma)
print('flag =', morph.flag)
print('flag_sersic =', morph.flag_sersic)

fig = make_figure(morph)
fig.savefig('output/statmorph_'+obj_name+'_'+filter_name+'.png', dpi=150)
plt.close(fig)
print(' Output Figure from stat morph saved in ./output.')




################################################################################################################
################################################################################################################
################################################################################################################

