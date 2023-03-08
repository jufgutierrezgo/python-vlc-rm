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
# Import SER 
from vlc_rm.ser import SymbolErrorRate
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import numpy as np
import pytest


class TestSER:

    SER_FLUX_VALUES = np.array(
            [9.6921e-01, 3.2325e-01, 9.5142e-02, 1.5848e-02, 1.4954e-03,
             1.1980e-04, 8.8000e-06, 2.0000e-07, 0.0000e+00]
            )

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

    pd1 = Photodetector(
        "PD2",
        position=[1.5, 1.5, 0.85],
        normal=[0, 0, 1],
        area=(1e-6)/3,
        # area=0.5e-4,
        fov=85,
        sensor='S10917-35GT',
        idark=1e-12
                )    

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
    
    channel_model = Recursivemodel("ChannelModelA", led1, pd1, room)
    channel_model.simulate_channel()
    
    ser = SymbolErrorRate(
            "SER-1",
            recursivemodel=channel_model,
            no_symbols=5e6
            )
    
    def test_attributes(self):
        assert self.ser._recursivemodel == self.channel_model
        assert self.ser.no_symbols == 5e6
    
    def test_rm_error(self):
        rm_errors = ['a', 1, [1, 2, 3], self.led1, self.pd1]

        for options in rm_errors:
            with pytest.raises(ValueError):
                ser = SymbolErrorRate(
                    "SER-1",
                    recursivemodel=options,
                    no_symbols=5e6
                    )
                
    def test_ser_validation(self):        
        self.ser.compute_ser_flux(
            min_flux=10,
            max_flux=10e3,
            points_flux=8
            )
        # print(repr(self.ser._ser_values))             
        assert np.allclose(
            self.ser._ser_values,
            self.SER_FLUX_VALUES,
            rtol=1e-1
                )
