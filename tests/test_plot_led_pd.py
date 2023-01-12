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

# test python package vlc-rm with 4-LEDs and 3-DETECTORS
def test_vlc_tled():

    Kt.NO_LEDS = 3

    led1 = Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        power=10,
        wavelengths=[620, 530, 460],
        fwhm=[20, 25, 20],
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

    plt.plot(
            led1._wavelenght,
            led1._led_spd[:,0],
            color='r',
            linestyle='solid'
        )
    plt.plot(
            led1._wavelenght,
            led1._led_spd[:,1],
            color='g',
            linestyle='solid'
        )
    plt.plot(
            led1._wavelenght,
            led1._led_spd[:,2],
            color='b',
            linestyle='solid'
        )

    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 1]/np.max(pd1._responsivity[:, 1:3]),
            color='r',
            linestyle='dashed'
        )
    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 2]/np.max(pd1._responsivity[:, 1:3]),
            color='g',
            linestyle='dashed'
        )
    plt.plot(
            pd1._responsivity[:, 0],
            pd1._responsivity[:, 3]/np.max(pd1._responsivity[:, 1:3]),
            color='b',
            linestyle='dashed'
        )
    plt.title("Spectral Response of LEDs and Detectors")
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Relative Spectrum and Response")
    plt.grid()
    plt.show()

