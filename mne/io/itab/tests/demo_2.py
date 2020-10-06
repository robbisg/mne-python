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

from mne.io.base import _BaseRaw


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
fpath = op.normpath('d:/data/rawdata/pzzdrn97_01')
 
fname = fpath + op.normpath('\pzzdrn97_0102.raw')
fname_fif = 'd:\RawData_Monk5_0107-raw.fif' 
fname_mhd = fname + ".mhd"
mhd = _read_mhd(fname_mhd)
info = _mhd2info(mhd)
pass

channel_indices = mne.pick_types(info, meg=True)  # MEG only

pass
#raw = read_raw_fif(fname_fif, preload=True, verbose=True)

raw = read_raw_itab(fname, preload=True, verbose=True)




print('sample rate:', raw.info['sfreq'], 'Hz')
print('channels x samples:', raw._data.shape)

#print(raw._data[1,1:20])
#array_data = raw._data[0, :1000]
#_ = plt.plot(array_data)

sc = dict(mag=2e+4, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
     emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4)

raw.plot(n_channels = 3, duration = 2, scalings = sc, block=True)

raw.plot_sensors(kind='3d', ch_type='mag')

#plt.plot(raw._data[0,:])
#plt.show()
