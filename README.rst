========
Overview
========

What is VLC-RM ?
================

VLC-RM is a package designed to simulate Visible Light Communication (VLC) systems based on Color Shift Keying 
modulation within indoor environments. The package calculates the propagation of light for multiple wavelengths 
in a rectangular empty room. Building upon a modified version of the Recursive Model (RM) presented in [1], 
this package provides the DC gain at each central wavelength. In order to compute this propagation, VLC-RM 
takes into account the spectral power distribution of multiple LEDs, the spectral response of the multiple 
color detectors, and the reflectance of the room's walls at central wavelengths. The spectral power distribution emitted by the LED-based transmitter is assumed to have a Gaussian shape, and the spatial intensity distribution is assumed to be a Lambertian radiator. A grid of points is used to discretize the room's walls into smaller square areas. The package executes a recursive algorithm to obtain the DC gain at each central wavelength and the minimum distance of the constellation. Based on the computation of the DC gain, the interchannel interference of the CSK-VLC system is estimated, along with the lighting parameters. The recursive algorithm assumes that the room's walls are perfect diffuse reflectors and that the transmitter is a point light source. The package simulates the transmission of CSK symbols through an Additive White Gaussian Noise (AWGN) channel. The received symbols are computed in the photodetected current space using the interchannel interference matrix and adding a gaussian noise.     


* Free software: BSD 3-Clause License

Installation
============

.. ::

..    pip install vlc-rm

.. You can also install the in-development version with::

You can install the in-development version with::

    pip install https://github.com/jufgutierrezgo/python-vlc-rm/archive/main.zip


An example of a VLC simulation
===============================

This example describes the usage of the VLC-RM package for characterizing a VLC system based on IEEE 16-CSK modulation within an empty rectangular space. The modulation 
is defined in [2]. 

Defining the VLC transmitter
----------------------------

The VLC system is composed of three elements: the LED-based transmitter, the photodetector, and the indoor environment (empty rectangular room). To define the transmitter of the VLC system is used the transmitter-module. The module must be imported,   and then a transmitter-type object 
is created as follows:

.. code-block:: python

    # Import Transmitter
    from vlc_rm.transmitter import Transmitter

    # Create a transmitter-type object
    transmitter = Transmitter(
        name="Led1",
        led_type='gaussian',
        reference='RGB-Phosphor',
        position=[1.34, 0.8, 2.30],
        normal=[0, 0, -1],
        mlambert=1.3,
        wavelengths=[620, 530, 475],
        fwhm=[20, 30, 20],
        constellation=constellation_white,
        luminous_flux=5000
                )
   
'transmitter' object is defined from seven parameters. The **led_type** parameter could are defined as 'gaussian' or 'custom'. When 'gaussian' is used the LED spectral emission is model as a gaussian shape. When 'custom' is used the LED spectral emission is model accordning with the data in `src/vlc_rm/led` folder. The **reference** parameter define the name of the .txt file when the custom mode is used. The **position** and **normal** parameters are defined by the 3D-cartesian coordinates. It means that the transmitter will be located in *[x=2.5, y=2.5, z=3]*. Through the **wavelengths** parameter, three central wavelengths (in nanometers) are fixed as *[620, 530, 475]*, which means that the transmitter uses three color red (620 nm), green (530 nm), and blue (475 nm). The **fwhm** parameter set the full width at half maximum (in nanometers) for each color LED as *[20, 30, 20]*. The **modulation** parameter defines the type of CSK modulation that can be simulated. **modulation** parameter is 'ieee16' as default. The **luminous_flux** (in Lumens) defines the average luminous flux emitted by the transmitter.
After defining the 'transmitter' module, the string representation of the object can be realized as follows: 

.. code-block:: python
    
    # Print the 'transmitter' object
    print(transmitter)
    

which produces an output similar to::

    List of parameters for LED transmitter: 
    Name: Led1
    Position [x y z]: [2.5000e+00 2.5000e+00 3.0000e+00] 
    Normal Vector [x y z]: [[0.0000e+00 0.0000e+00 -1.0000e+00]] 
    Lambert Number: 1.0 
    Central Wavelengths [nm]: [6.2000e+02 5.3000e+02 4.7500e+02] 
    FWHM [nm]: [2.0000e+01 3.0000e+01 2.0000e+01]
    Luminous Flux [lm]: 5000.0
    Correlated Color Temperature: [[-4.3902e+06]]
    CIExy coordinates: [[2.3633e-01 1.9580e-01 5.6787e-01]]
    ILER [W/lm]: 
    [[3.8001e-03 0.0000e+00 0.0000e+00]
    [0.0000e+00 1.8197e-03 0.0000e+00]
    [0.0000e+00 0.0000e+00 1.1960e-02]] 
    Average Power per Channel Color: 
    [6.3336e+00 3.0328e+00 1.9934e+01] 
    Total Power emmited by the Transmitter [W]: 
    29.30032767693627 
 

The spectral power distribution of the LED transmitter according to the central wavelengths,
the FWDM, and the luminous flux can be plotted with:

.. code-block:: python
    
    # Plot the normalized spectral power distribution 
    transmitter.plot_spd_normalized()
    
The output image is:

.. image:: images_example/spd_norm.png

 


Defining the VLC photodetector
------------------------------

To define the photodetector is used the photodetector-module. The module must be imported 
and creating a photodetector-type object as follows:

.. code-block:: python

    pd = Photodetector(
        "PD1",
        position=[0.5, 0.5, 0.85],
        normal=[0, 0, 1],
        area=(1e-4)/3,
        fov=85,
        sensor='S10917-35GT',        
        idark=1e-12,
        gain=3e5
                )


'photodetector' object is defined from six parameters. The **position** parameter 
is defined as a three-dimensional array that represents the 3D-cartesian coordinate. The position 
is equal to *[x=0.5, y=1.0, z=0.85]*. The normal vector to the LED's area is configured 
through the **normal** parameter, which is equal to *[0, 0, 1]*. 
The **area** parameter is configured equal to *(1e-4)/3* (square meters), and it represents the 
active area of the photodetector. The **field-of-view** parameter defines the solid angle through 
which a detector is sensitive, and for this example, it is 85. The **sensor** parameter represents 
the detector reference which defines the spectral responsivity of the optical-to-electrical conversion. 
The **idark** parameter represents the dark current of photodetector. The **gain** parameter represents 
transconductance amplifier gain used to digitalize the received signal. Getting the available sensor 
list by using the next command:

.. code-block:: python

    pd.list_sensors()

The **idark** parameter defines the dark current of the photodetector and it is set as
**1e-12**. After defining the 'transmitter' module, the string representation of 
the object can be realized as follows:

After defining the 'photodetetor' module, the string representation of the object can be realized as follows:  

.. code-block:: python
    
    # Print the 'transmitter' object
    print(pd)
    

which produces an output similar to::

    List of parameters for photodetector PD1: 
    Name: PD1 
    Position [x y z]: [5.0000e-01 5.0000e-01 8.5000e-01] 
    Normal Vector [x y z]: [[0.0000e+00 0.0000e+00 1.0000e+00]] 
    Active Area[m2]: 3.333333370392211e-05 
    FOV: 85.0 
    Sensor: S10917-35GT


The spectral responsivity of the photodetector can be plotted as:

.. code-block:: python
    
    # Plot the normalized spectral power distribution 
    pd.plot_responsivity()
   
The output image is:

.. image:: images_example/responsivity.png

Defining the VLC Indoor Environment
-----------------------------------

The indoor space for VLC is defined by using the 'IndoorEnv' module. The **size** parameter (in meters)
specifies the length, width, and height of the rectangular room. This parameter is defined 
as the three-dimensional array **[5, 5, 3]**. The **no_reflections** 
parameter specifies the order of reflection to compute the lighting parameters and 
the interchannel interference. The package support from 0-order to 10-order of reflection. 
The reflectance at the central wavelengths of each wall can be defined. 
The **resolution** parameter (in meters) determines the length 
of the smaller square areas. The accuracy of the model depends on the resolution.  

.. code-block:: python

    room = Indoorenv(
        "Room",
        size=[5, 5, 3],
        no_reflections=10,
        resolution=1/10,
        ceiling=[0.82, 0.71, 0.64],
        west=[0.82, 0.71, 0.64],
        north=[0.82, 0.71, 0.64],
        east=[0.82, 0.71, 0.64],
        south=[0.82, 0.71, 0.64],
        floor=[0.635, 0.61, 0.58]
            )


The 'create_environment()' method  is used to create a grid 
of points and two pairwise parameters of the indoor environment [Article Reference].

.. code-block:: python

    room.create_environment()

if this method computes the grid and pairwise parameters correctly, it 
produces an output similar to ::


    Creating parameters of indoor environment ...
    Parameters created!


Simulate the indoor VLC system
------------------------------

The simulation of the indoor CSK-based VLC is carried out by the 'RecursiveModel' module, which is defined as follows.

.. code-block:: python

    # Define Channel Model
    channel_model = Recursivemodel(
        "ChannelModelA",
        transmitter,
        pd,
        room
        )

the 'channel_model' is an object that is defined from the **transmitter**, **pd**, and **room** objects. The 
channel simulation is executed through the 'simulate_channel()' method.


.. code-block:: python
    
    # Simulate indoor channel
    channel_model.simulate_channel()    

if this method simulates successfully, it produces an output similar to ::

    Creating parameters of indoor environment ...
    Parameters created!


To Get the simulation results can be used the print function:

.. code-block:: python

    # Print results of the simulation
    print(channel_model)   

obtaining an output similar to::

    |=============== Simulation results ================|
    Name: ChannelModelA 
    DC-Gain with respect to 1-W [W]: 
    [2.0031e-06 1.7320e-06 1.6059e-06] 
    Crosstalk Matrix at 1-lm: 
    [[1.1988e-09 2.1790e-13 6.5149e-14]
    [1.8048e-11 6.1623e-10 2.7827e-10]
    [6.2127e-12 1.0141e-10 3.5986e-09]] 
    Crosstalk Matrix at 5000.0-lm: 
    [[5.9941e-06 1.0895e-09 3.2574e-10]
    [9.0238e-08 3.0812e-06 1.3914e-06]
    [3.1064e-08 5.0706e-07 1.7993e-05]] 
    Crosstalk Matrix with photodetector gain of 300000.0: 
    [[1.7982e+00 3.2685e-04 9.7723e-05]
    [2.7071e-02 9.2435e-01 4.1741e-01]
    [9.3191e-03 1.5212e-01 5.3979e+00]] 
    Lighting Parameters at 5000.0-lm 
    Illuminance [lx]: [[2.6705e+02]] 
    CIExyz: [[2.5739e-01 2.0525e-01 5.3736e-01]] 
    CCT: [[-3.8330e+06]] 
    CRI: [[1.4302e+01]] 
    Min-Distance: 4.140491133537268e-10  


The VLC-RM package reports the radiometric power received at the photodetector
when each LED radiates 1 W. The Crosstalk matrix at the luminous flux is reported.
This matrix related the transmitted symbols represented in the luminous flux space,
and the received symbols represented in the current space. The minimum distance 
is reported according to the Crosstalk matrix, and the constellation 
at the transmitter. The illuminance, the CIE color coordinates, 
and the color rendering index are reported. The VLR-RM uses the Luxpy Python 
package (https://pypi.org/project/luxpy/) to compute photometric and colorimetric indexes.

Notebooks with practical examples
=================================

The **examples** folder contains some useful Jupyter python examples for a basic usage of the VLC-RM package. 


.. Documentation
.. =============


.. https://python-vlc-rm.readthedocs.io/


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