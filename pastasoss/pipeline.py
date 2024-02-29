"""
Module to write PWCPOS sensitive wavemap and spectrace data to new reference files

Author: Joe Filippazzo
Date: 02/28/2024
Usage:
import pastasoss
pwcpos = 245.8
pastasoss.write_soss_reffiles(pwcpos, 'my_new_wavemap.fits', 'my_new_spectrace.fits')
"""

import shutil
from pkg_resources import resource_filename

from astropy.io import fits

from pastasoss import get_soss_wavemaps


def write_soss_reffiles(pwcpos, wavemap_filepath, spectrace_filepath):
    """
    Generate wavemap reference files given a PWCPOS value

    Parameters
    ----------
    pwcpos : float
        The pupil wheel position to use
    wavemap_filepath : str
        The filepath for the new reference file
    template : str
        The reference file to use as a template
    """
    # Get the template reference files
    spectrace_template = resource_filename('pastasoss', 'pastasoss/data/jwst_niriss_spectrace_template.fits')
    wavemap_template = resource_filename('pastasoss', 'pastasoss/data/jwst_niriss_wavemap_template.fits')

    # Generate the padded wavemap
    wavemaps, spectraces = get_soss_wavemaps(pwcpos, padding=True, spectraces=True)

    # Copy the spectrace reference file and replace the data with that generated by pastasoss
    shutil.copy(spectrace_template, spectrace_filepath)
    with fits.open(spectrace_filepath, mode='update') as hdul:
        for order, spectrace in enumerate(spectraces):
            trace_data = hdul[order + 1].data
            trace_data.X = spectrace[0]
            trace_data.Y = spectrace[1]

    print('New spectrace reference file saved:', spectrace_filepath)

    # Copy the tamplate wavemap reference file and replace the data with that generated by pastasoss
    shutil.copy(wavemap_template, wavemap_filepath)
    with fits.open(wavemap_filepath, mode='update') as hdul:
        for order, wmap in enumerate(wavemaps):  # Keep reffile order 3 wavemap for now
            wmap_data = hdul[order + 1].data
            wmap_data = wmap

    print('New wavemap reference file saved:', wavemap_filepath)