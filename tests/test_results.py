import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import matplotlib.pyplot as plt

import numpy as np

from numpy import loadtxt

# test python package vlc-rm with 4-LEDs and 3-DETECTORS
def test_vlc_tled():

    Kt.NO_LEDS = 3

    led1 = Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        power=10,
        wavelengths=[620, 530, 470],
        fwhm=[15, 25, 18],
        modulation='ieee16',
        luminous_flux=600
                )
    # led1.led_pattern()
    # led1.plot_spd_led()
    print(led1)

    pd1 = Photodetector(
        "PD1",
        position=[0.5, 1.0, 0],
        normal=[0, 0, 1],
        area=1e-4,
        fov=85,
        sensor='S10917-35GT'
                )
    # pd1.plot_responsivity()
    print(pd1)

    # load the spectral reflectance of Plaster material
    walls_reflectance = loadtxt(
        "/home/juanpc/python_phd/cruft_sample/python-vlc-rm/tests/Interp_ReflecPlaster.txt"
        )
    floor_reflectance = loadtxt(
        "/home/juanpc/python_phd/cruft_sample/python-vlc-rm/tests/Interp_ReflecFloor.txt"
        )
    plt.plot(
            walls_reflectance[:, 0],
            walls_reflectance[:, 1],
            color='black',
            linestyle='solid',
            label='Walls-Reflectance'
        )
    plt.plot(
            floor_reflectance[:, 0],
            floor_reflectance[:, 1],
            color='black',
            linestyle='dashed',
            label='Floor-Reflectance'
        )
    plt.plot(
            led1._wavelenght,
            led1._led_spd[:, 0],
            color='r',
            linestyle='solid',
            label='Red-LED'
        )
    plt.plot(
            led1._wavelenght,
            led1._led_spd[:, 1],
            color='g',
            linestyle='solid',
            label='Green-LED'
        )
    plt.plot(
            led1._wavelenght,
            led1._led_spd[:, 2],
            color='b',
            linestyle='solid',
            label='Blue-LED'
        )

    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 1]/np.max(pd1._responsivity[:, 1:3]),
            color='r',
            linestyle='dashed',
            label='Red-Detector'
        )
    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 2]/np.max(pd1._responsivity[:, 1:3]),
            color='g',
            linestyle='dashed',
            label='Green-Detector'
        )
    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 3]/np.max(pd1._responsivity[:, 1:3]),
            color='b',
            linestyle='dashed',
            label='Blue-Detector'
        )

    
    #plt.title("Spectral Response of LEDs and Detectors", fontsize=20)
    plt.xlabel("Wavelength [nm]", fontsize=16)
    plt.ylabel("Relative Spectrum and Response",  fontsize=16)
    plt.grid()
    plt.legend(
        loc="upper left", 
        fontsize=12, 
        bbox_to_anchor=[0, 1],
        ncol=1, 
        #shadow=True, 
        #fancybox=True
        )
    plt.xlim([400, 700])
    plt.ylim([0, 1.1])
    plt.show()
