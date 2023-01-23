import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Indoor Environment
from vlc_rm.indoorenv import Indoorenv
# Import REcursiveModel
from vlc_rm.recursivemodel import Recursivemodel
# Import Symbol Error Rate 
from vlc_rm.ser import SymbolErrorRate
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import numpy as np

# test python package vlc-rm with 4-LEDs and 3-DETECTORS
def test_vlc_tled():

    Kt.NO_LEDS = 3

    led1 = Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        wavelengths=[620, 530, 475],
        fwhm=[20, 45, 20],
        modulation='ieee16',
        luminous_flux=5000
                )
    # led1.led_pattern()
    # led1.plot_spd_led()
    print(led1)    

    pd1 = Photodetector(
        "PD1",
        position=[2.5, 2.5, 0.85],
        normal=[0, 0, 1],
        area=(1e-6)/3,
        # area=0.5e-4,
        fov=85,
        sensor='S10917-35GT'
                )
    # pd1.plot_responsivity()
    print(pd1)

    room = Indoorenv(
        "Room",
        size=[5, 5, 3],
        no_reflections=10,
        resolution=1/8,
        ceiling=[0.82, 0.71, 0.64],
        west=[0.82, 0.71, 0.64],
        north=[0.82, 0.71, 0.64],
        east=[0.82, 0.71, 0.64],
        south=[0.82, 0.71, 0.64],
        floor=[0.635, 0.61, 0.58]
            )

    room.create_envirorment(led1, pd1)
    print(room)

    channel_model = Recursivemodel("ChannelModelA", led1, pd1, room)
    channel_model.simulate_channel()
    print(channel_model)
    #channel_model.print_Hk()
    channel_model._plot_spd()  
    # print(channel_model._avg_power) 

    ser1 = SymbolErrorRate(
            "SER-1",
            recursivemodel=channel_model,
            no_symbols=1e6
            )
    
    # ser1.compute_ser_snr(        
    #     min_snr=0,
    #    max_snr=40,
    #    points_snr=10
    #    )
    ser1.compute_ser_flux(
        min_flux=10,
        max_flux=1.5e4,
        points_flux=10
        )
    print(ser1)     
    ser1.plot_ser(mode='flux')
    ser1.save_SerFLux_data()

    """
    print("\n CSK symbols payload")
    print(ser1._symbols_csk)
    print("\n CSK symbols frame transmitted noiseless")
    print(ser1._symbols_transmitted)
    print("\n CSK symbols frame transmitted with noise")
    print(ser1._noise_symbols)
    print("\n RX header")
    print(ser1._rx_header)    
    print("\n Inverse Symbols")
    print(ser1._inverse_rx_symbols)
    print("\n Original symbols")
    print(ser1._symbols_decimal)
    print("\n Decoded symbols")
    print(ser1._index_min)
    print("\n Symbol error rate")
    print(ser1._error_rate)
    """

    assert (
        channel_model._channel_dcgain[0] > 2.43e-06 and channel_model._channel_dcgain[0] < 2.44e-06
        # channel_model.rgby_dcgain[0] == 2.5e-06
        )