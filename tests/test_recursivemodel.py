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
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import numpy as np
import pytest


class TestHappyRM:

    transmitter = Transmitter(
            "Led1",
            position=[2.5, 2.5, 3],
            normal=[0, 0, -1],
            mlambert=1,
            wavelengths=[620, 530, 475],
            fwhm=[20, 45, 20],
            modulation='ieee16',
            luminous_flux=5000
                    )

    photodetector = Photodetector(
            "PD2",
            position=[0.5, 1, 0],
            normal=[0, 0, 1],
            area=1e-4,
            # area=0.5e-4,
            fov=85,
            sensor='S10917-35GT',
            idark=1e-12
                )

    indoor_env = Indoorenv(
            "Room",
            size=[5, 5, 3],
            no_reflections=3,
            resolution=1/8,
            ceiling=[0.8, 0.8, 0.8],
            west=[0.8, 0.8, 0.8],
            north=[0.8, 0.8, 0.8],
            east=[0.8, 0.8, 0.8],
            south=[0.8, 0.8, 0.8],
            floor=[0.3, 0.3, 0.3]
                )

    indoor_env.create_envirorment(transmitter, photodetector)
    channel_model = Recursivemodel(
        "ChannelModelA",
        transmitter,
        photodetector,
        indoor_env
        )
    channel_model.simulate_channel()
    print(channel_model)

    def test_attributes(self):
        assert self.channel_model._led == self.transmitter
        assert self.channel_model._photodetector == self.photodetector
        assert self.channel_model._room == self.indoor_env


    def test_dcgain_validation(self):        
        for channel in range(Kt.NO_LEDS):
            assert self.channel_model._channel_dcgain[0] > 2.43e-06
            assert self.channel_model._channel_dcgain[0] < 2.44e-06

    def test_illuminance(self):
        assert self.channel_model.illuminance > 1.2165e+02
        assert self.channel_model.illuminance < 1.2166e+02
