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

* Transmitter module: 
    The module has a set of attributes to define the LED-based transmitter characteristics.
    The module computes the spectral power distribution assuming a gaussian shape, and the 
    spatial intensity distribution according to a Lambertian radiator.

    | Properties:    
    | ├── Name 
    | ├── Position 
    | ├── Normal vector 
    | ├── Central wavelengths 
    | ├── Full width at half maximum 
    | ├── Number of Lambertian radiator 
    | ├── Luminous flux 
    | ├── Luminous efficacy of radiation 
    | ├── Average power per channel 
    | ├── Spectral power distribution 
    |
    | Functions:    
    | ├── Plot spatial distribution
    | ├── Plot SPD at 1 lumen
    | ├── Plot normalized SPD
    | ├── Print properties

* Photodetector module:
    The module has a set of attributes to define the photodetector characteristics.    

    | Properties:    
    | ├── Name 
    | ├── Position 
    | ├── Normal vector 
    | ├── Active area 
    | ├── Full width at half maximum 
    | ├── Spectral responsivity
    | ├── Field of view
    | ├── Dark current
    |
    | Functions:    
    | ├── Plot spectral responsivity
    | ├── Print properties

* Indoor Environment module:
    The module has a set of attributes to define the empty rectangular room where the
    light wave propagates. The module calculates a grid of points to discretize the surface of 
    walls into square smaller areas. It also computes the pairwise distance and the cosine angle between 
    the points of the grid.   

    | Properties:    
    | ├── Name 
    | ├── Size of the room
    | ├── Resolution for grid of points
    | ├── Reflectace at each wall at central wavelengths
    | ├── Number of reflection order.
    |
    | Functions:    
    | ├── Create grid 
    | ├── Compute pirwise parameters 
    | ├── Print properties

* Recursive Model module:
    The module has a set of attributes to execute a recursive algorithm by gettig a DC gain 
    at each central wavelength, and the minimum distance of the constellation. 
    Based on DC gain computation, the interchannel interferce of the 
    CSK-VLC system is estimated, as well as lighting parameters. The recursive model assummes 
    that room's walls are perfect diffusse reflectors and a transmitter a point light source.
    
    | Properties:    
    | ├── Name 
    | ├── DC gain at central wavelengths
    | ├── Interchannel interference matrix
    | ├── Minimum distance
    | ├── Lighting parameters at detector position  
    |       ├── Illuminance
    |       ├── Correlated color temperature
    |       ├── Color rendering index
    |       ├── CIExy coordinates
    |
    | Functions:    
    | ├── Simulate channel
    | ├── Print DC gain at each reflection order
    | ├── Print DC gain at each central wavelength
    | ├── Plot the receive constellation
    | ├── Print properties


* Symbols-Error-Rate (SER) module: 
    The module has a set of attributes to simulated a transmission of CSK symbols 
    through an AWGN channel. Using the interchannel interference matrix estimated 
    with the Recursive Model module, this module computes the received symbols in the current space, 
    adds gaussian noise and calculates the symbols error rate of the tranmission.  

    | Properties:    
    | ├── Name 
    | ├── Number of symbols to transmit
    | ├── Symbol error rate
    |
    | Functions:    
    | ├── Computes symbol error rate
    | ├── Plot symbol error rate vs. transmitter's luminous flux 
    | ├── Save data to file
    


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