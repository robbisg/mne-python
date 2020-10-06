"""Conversion tool from ITAB to FIF
"""

# Author: Vittorio Pizzella <vittorio.pizzella@unich.it>
#
# License: BSD (3-clause)

import numpy as np

from ...utils import verbose
from ..base import BaseRaw
from ..utils import _mult_cal_one
from ...utils import logger
from .mhd import _read_mhd
from .info import _mhd2info

class RawITAB(BaseRaw):
    """Raw object from ITAB directory

    Parameters
    ----------
    fname : str
        The raw file to load. Filename should end with *.raw
    preload : bool or str (default False)
        Preload data into memory for data manipulation and faster indexing.
        If True, the data will be preloaded into memory (fast, requires
        large amount of memory). If preload is a string, preload is the
        file name of a memory-mapped file which is used to store the data
        on the hard drive (slower, requires less memory).
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).

    See Also
    --------
    mne.io.Raw : Documentation of attribute and methods.
    """
    
    @verbose
    def __init__(self, fname, preload=False, verbose=True):


        #if preload:    
        #    self._preload_data(preload)
        #else:
        #    self.preload = False
        
        filenames = list()
        filenames.append(fname)
        
        fname_mhd = fname + ".mhd"
        mhd = _read_mhd(fname_mhd)  # Read the mhd file
        info = _mhd2info(mhd)
        info['buffer_size_sec'] = info['n_samp'] / info['sfreq']
        logger.info(int(info['buffer_size_sec']))

        if info.get('buffer_size_sec', None) is None:
            raise RuntimeError('Reader error, notify mne-python developers')
        self.info = info
        #self.n_times = info['n_samp']
        #self.times = info['n_samp']
        info._check_consistency()
        
        first_samps = [0]
        last_samps = [info['n_samp'] - 1]
        self.verbose = verbose

        raw_extras = list()
        for fi, _ in enumerate(filenames):
            raw_extras.append(dict())
            for k in ['n_samp', 'start_data', 'nchan']:
                raw_extras[fi][k] = self.info[k]

        super(RawITAB, self).__init__(info, preload, 
                                      last_samps=last_samps,
                                      raw_extras=raw_extras,
                                      filenames=filenames,
                                      verbose=verbose)





    def _read_segment_file(self, data, idx, fi, start, stop, cals, mult):
        """Read a segment of data from a file.
        Only needs to be implemented for readers that support
        ``preload=False``.
        Parameters
        ----------
        data : ndarray, shape (len(idx), stop - start + 1)
            The data array. Should be modified inplace.
        idx : ndarray | slice
            The requested channel indices.
        fi : int
            The file index that must be read from.
        start : int
            The start sample in the given file.
        stop : int
            The stop sample in the given file (inclusive).
        cals : ndarray, shape (len(idx), 1)
            Channel calibrations (already sub-indexed).
        mult : ndarray, shape (len(idx), len(info['chs']) | None
            The compensation + projection + cals matrix, if applicable.
        """
        
        # Initial checks
        start = int(start)
        if stop is None or stop > self._raw_extras[fi]['n_samp']:
            stop = self._raw_extras[fi]['n_samp']

        if start >= stop:
            raise ValueError('No data in this range')

        data_offset = self._raw_extras[fi]['start_data']

        n_samp = stop - start

        with open(self._filenames[fi], 'rb') as fid:

            #position  file pointer
            fid.seek(data_offset + start * self._raw_extras[fi]['nchan'], 0)

            # read data                
            n_read = self._raw_extras[fi]['nchan'] * n_samp

            this_data = np.fromfile(fid, '>i4', count=n_read)
            this_data.shape = (n_samp, self._raw_extras[fi]['nchan'])

            # calibrate data
            _mult_cal_one(data, this_data.transpose(), idx, cals, mult)
            


def read_raw_itab(fname, preload=False, verbose=None):
    """Raw object from ITAB directory

    Parameters
    ----------
    fname : str
        The raw file to load. Filename should end with *.raw
    preload : bool or str (default False)
        Preload data into memory for data manipulation and faster indexing.
        If True, the data will be preloaded into memory (fast, requires
        large amount of memory). If preload is a string, preload is the
        file name of a memory-mapped file which is used to store the data
        on the hard drive (slower, requires less memory).
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).

    Returns
    -------
    raw : instance of RawITAB
        The raw data.

    See Also
    --------
    mne.io.Raw : Documentation of attribute and methods.

    Notes
    -----
    .. versionadded:: 0.01
    """
    
    a = RawITAB(fname, preload=preload, verbose=verbose)
    return a