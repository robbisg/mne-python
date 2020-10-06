# Authors: Vittorio Pizzella <vittorio.pizzella@unich.it>
#
# License: BSD (3-clause)

import os
import mne
from os import path as op
import shutil
import warnings
import time

import numpy as np

import matplotlib.pyplot as plt

from nose.tools import assert_raises, assert_true, assert_false
from numpy.testing import assert_allclose, assert_array_equal, assert_equal

from mne.externals.six import string_types


from mne import pick_types
from mne.tests.common import assert_dig_allclose
from mne.transforms import apply_trans
from mne.io import Raw

from mne.io.base import BaseRaw

from mne.utils import logger

from mne.io.constants import FIFF

from mne.io.itab.mhd import _read_mhd
from mne.io.itab.info import _mhd2info
from mne.io.itab.itab import read_raw_itab


def _make_itab_name(directory, extra, raise_error=True):
    """Helper to make a ITAB name"""
    fname = op.join(directory, op.basename(directory)[:-3] + '.' + extra)
    if not op.isfile(fname):
        if raise_error:
            raise IOError('Standard file %s not found' % fname)
        else:
            return None
    return fname


pass
fname =''
fpath = op.normpath('d:/data/rawdata/laefba85_02')

fname = fpath + op.normpath('/laefba85_0201.raw'); 


#fname_mhd = fname + ".mhd"
#mhd = _read_mhd(fname_mhd)
#info = _mhd2info(mhd)
#channel_indices = mne.pick_types(info, meg=True)  # MEG only

raw = read_raw_itab(fname, preload=True, verbose=True)

channel_indices = mne.pick_types(raw.info, meg=True)  # MEG only

raw.save('d:/data/rawdata/laefba85_02/test.fif', tmin=0, tmax=150,
         picks=channel_indices, overwrite=True)

print('sample rate:', raw.info['sfreq'], 'Hz')
print('channels x samples:', raw._data.shape)
print('dig points',raw.info['dig'])

sc = dict(mag=2e+4, grad=4e-11, eeg=20e-4, eog=150e-6, ecg=5e-4,
     emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4)

raw.plot(n_channels = 5, duration = 2, scalings = sc, block=True)

raw.plot_sensors(kind='3d', ch_type='mag')