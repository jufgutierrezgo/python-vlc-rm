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
================

VLC-RM is a package designed to simulate Visible Light Communication (VLC) systems based on Color Shift Keying 
modulation within indoor environments. The package calculates the propagation of light for multiple wavelengths 
in a rectangular empty room. Building upon a modified version of the Recursive Model (RM) presented in [1], 
this package provides the DC gain at each central wavelength. In order to compute this propagation, VLC-RM 
takes into account the spectral power distribution of multiple LEDs, the spectral response of the multiple 
color detectors, and the reflectance of the room's walls at central wavelengths. The spectral power distribution 
emitted by the LED-based transmitter is assumed to have a Gaussian shape, and the spatial intensity distribution 
is assumed to be a Lambertian radiator. A grid of points is used to discretize the room's walls into smaller square areas.

The package executes a recursive algorithm to obtain the DC gain at each central wavelength and the minimum 
distance of the constellation. Based on the computation of the DC gain, the interchannel interference of the CSK-VLC 
system is estimated, along with the lighting parameters. The recursive algorithm assumes that the room's walls are 
perfect diffuse reflectors and that the transmitter is a point light source. The package simulates the transmission 
of CSK symbols through an Additive White Gaussian Noise (AWGN) channel. The received symbols are computed in the 
photodetected current space using the interchannel interference matrix and adding a gaussian noise.     


* Free software: BSD 3-Clause License

Installation
============

::

    pip install vlc-rm

You can also install the in-development version with::

    pip install https://github.com/jufgutierrezgo/python-vlc-rm/archive/main.zip



An example of VLC simualtion
============================

This example describes the usage of the VLC-RM package for characterizing a VLC system 
based on IEEE 16-CSK modulation within an empty rectangular space. The modulation 
is defined in [2]. 

Defining basic elements
------------------------

The VLC system is composed by three elements: the LED-based transmitter, the photodetector, 
and the indoor environment (empty rectangular room). To defined the LED-based transmitter 
is used the transmitter-module. The module must be imported and creating a transmitter-type object:

.. code-block:: python

    # Import Transmitter
    from vlc_rm.transmitter import Transmitter

    transmitter = Transmitter(
            "Led1",
            position=[2.5, 2.5, 3],
            normal=[0, 0, -1],
            mlambert=1,
            wavelengths=[620, 530, 475],
            fwhm=[20, 30, 20],
            modulation='ieee16',
            luminous_flux=5000
                    )

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

[2] IEEE Standards Association. (2019). IEEE Standard for Local and metropolitan area networks—Part 15.7: 
Short-Range Optical Wireless Communications (IEEE Std 802.15.7-2018, Revision of IEEE Std 802.15.7-2011) (pp. 1-407). 
https://ieeexplore.ieee.org/document/8697198