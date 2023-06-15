========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-vlc-rm/badge/?style=flat
    :target: https://python-vlc-rm.readthedocs.io/
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/vlc-rm.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/vlc-rm

.. |wheel| image:: https://img.shields.io/pypi/wheel/vlc-rm.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/vlc-rm

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/vlc-rm.svg
    :alt: Supported versions
    :target: https://pypi.org/project/vlc-rm

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/vlc-rm.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/vlc-rm

.. |commits-since| image:: https://img.shields.io/github/commits-since/jufgutierrezgo/python-vlc-rm/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jufgutierrezgo/python-vlc-rm/compare/v0.0.0...main



.. end-badges

What is VLC-RM ?
============

VLC-RM is a package designed to simulated Visible Light Communication (VLC) systems 
based on Color Shift Keying modulation inside of indoor environments. The package 
computes the light propagation for multiple wavelengths in a rectagular empty room. From a 
modified version of the Recursive Model (RM) presented [1], this package reports 
the DC gain at each central wavelengths. To compute this propagation, VLC-RM considers 
the spectral power distribution of multiple LEDs, the spectral response of the multiple 
color detectors, and the room's walls reflectance at central wavelengths. 

VLC-RM is composed of 5 modules:

#. Transmitter module:

#. Photodetector module:

#. Room module:

#. Recursive-model module:

#. Symbols Error Rate module: 




* Free software: BSD 3-Clause License

Installation
============

::

    pip install vlc-rm

You can also install the in-development version with::

    pip install https://github.com/jufgutierrezgo/python-vlc-rm/archive/main.zip


Documentation
=============


https://python-vlc-rm.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

References
===========

[1] Barry, J. R., Kahn, J. M., Krause, W. J., Lee, E. A., & Messerschmitt, D. G. (1993). 
Simulation of multipath impulse response for indoor wireless optical channels. IEEE journal on selected areas in communications, 11(3), 367-379.