.. NOTE: we are now using links to highlight new functions and classes.
   Please follow the examples below like :func:`mne.stats.f_mway_rm`, so the
   whats_new page will have a link to the function/class documentation.

.. NOTE: there are 3 separate sections for changes, based on type:
   - "Enhancements" for new features
   - "Bugs" for bug fixes
   - "API changes" for backward-incompatible changes

.. _current:

Current (0.22.dev0)
-------------------

Enhancements
~~~~~~~~~~~~

- Speed up :class:`mne.decoding.TimeDelayingRidge` with edge correction using Numba by `Eric Larson`_ (:gh:`8323`)

- The ``max_pca_components`` argument of `~mne.preprocessing.ICA` can now be a float between 0.0 and 1.0, allowing users to specify a relative amount of cumulative explained variance. This can be used to exclude "unimportant" principal components, thereby conducting a rank reduction of the data, by `Richard Höchenberger`_ (:gh:`8321`)

- `~mne.preprocessing.ICA` has gained a new attribute ``max_pca_components_``, which will be set when calling `~mne.preprocessing.ICA.fit`, by `Richard Höchenberger`_ (:gh:`8321`)

Bugs
~~~~

- Fix bug with :func:`mne.viz.plot_source_estimates` when using the PyVista backend where singleton time points were not handled properly by `Eric Larson`_ (:gh:`8285`)

- Fix bug with compensated CTF data when picking channels without preload by `Eric Larson`_ (:gh:`8318`)

- Fix bug when merging fNIRS channels in :func:`mne.viz.plot_evoked_topomap` and related functions by `Robert Luke`_ (:gh:`8306`)

- :func:`mne.io.read_raw_edf` now supports EDF files with invalid recording dates by `Clemens Brunner`_ (:gh:`8283`)

- Fix bug with :ref:`somato-dataset` where the BEM was not included by `Eric Larson`_ (:gh:`8317`)

- Fix missing documentation of :func:`mne.io.read_raw_nihon` in :ref:`tut-imorting-eeg-data` by `Adam Li`_ (:gh`8320`)

- Fix bug with :func:`mne.add_reference_channels` when :func:`mne.io.Raw.reorder_channels` or related methods are used afterward by `Eric Larson`_ (:gh:`8303`)

- ``ICA.max_pca_components`` will not be altered by calling `~mne.preprocessing.ICA.fit` anymore. Instead, the new attribute ``ICA.max_pca_components_`` will be set, by `Richard Höchenberger`_ (:gh:`8321`)


API changes
~~~~~~~~~~~

...
