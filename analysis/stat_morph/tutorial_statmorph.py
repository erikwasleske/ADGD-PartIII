import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import simple_norm
from astropy.modeling.models import Sersic2D
from astropy.convolution import convolve, Gaussian2DKernel
from photutils.segmentation import detect_threshold, detect_sources
import time
import statmorph
from statmorph.utils.image_diagnostics import make_figure
#matplotlib inline
#################################################################
############################
#######   TUTORIAL   #######
############################
### TRY FIRST WITH FAKE MODEL:
plt.interactive(True)

# create model galaxy image:
ny, nx = 240, 240
y, x = np.mgrid[0:ny, 0:nx]
sersic_model = Sersic2D(
    amplitude=1, r_eff=20, n=2.5, x_0=120.5, y_0=96.5,
    ellip=0.5, theta=0.5)
image = sersic_model(x, y)
plt.imshow(image, cmap='gray', origin='lower',
           norm=simple_norm(image, stretch='log', log_a=10000))
#plt.show(block=True)
print('Created Model Image')

# convolve with psf:
kernel = Gaussian2DKernel(2)
kernel.normalize()  # make sure kernel adds up to 1
psf = kernel.array  # we only need the numpy array
plt.imshow(psf, origin='lower', cmap='gray')
#plt.show(block=True)
print('Created model psf')


image = convolve(image, psf)
plt.imshow(image, cmap='gray', origin='lower',
           norm=simple_norm(image, stretch='log', log_a=10000))
#plt.show(block=True)
print('Convolved imaged with psf.')

# applying shot noise
np.random.seed(3)
gain = 1e5
image = np.random.poisson(image * gain) / gain
print('applied shot noise')

# apply background noise:
snp = 100.0
sky_sigma = 1.0 / snp
image += sky_sigma * np.random.standard_normal(size=(ny, nx))
plt.imshow(image, cmap='gray', origin='lower',
           norm=simple_norm(image, stretch='log', log_a=10000))
plt.show(block=True)
print(' applied bkgrd noise.')

# creating segmentaion map
threshold = detect_threshold(image, 1.5)
npixels = 5  # minimum number of connected pixels
convolved_image = convolve(image, psf)
segmap = detect_sources(convolved_image, threshold, npixels)
plt.imshow(segmap, origin='lower', cmap='gray')
plt.show(block=True)

#################################################################
### RUNNING STATMORPH
start = time.time()
source_morphs = statmorph.source_morphology(
    image, segmap, gain=gain, psf=psf)
print('Time: %g s.' % (time.time() - start))
morph = source_morphs[0]

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
fig.savefig('output/tutorial.png', dpi=150)
plt.close(fig)
########################################################
########################################################
########################################################
