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

import pytest


@pytest.fixture
def transmitter():
    return Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        wavelengths=[620, 530, 475],
        fwhm=[20, 45, 20],
        modulation='ieee16',
        luminous_flux=5000
                )

@pytest.fixture
def photodetector():
    return Photodetector(
        "PD2",
        position=[0.5, 1, 0],
        normal=[0, 0, 1],
        area=1e-4,
        # area=0.5e-4,
        fov=85,
        sensor='S10917-35GT',
        idark=1e-12
            )

@pytest.fixture
def indoor_env():
    return Indoorenv(
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
        

class TestRecursiveModule:   
        
    def test_attributes(self, transmitter, photodetector, indoor_env):
        
        indoor_env.create_envirorment(transmitter, photodetector)
        channel_model = Recursivemodel("ChannelModelA", transmitter, photodetector, indoor_env)                   
        
        assert (
            channel_model._led == transmitter and
            channel_model._photodetector == photodetector and
            channel_model._room == indoor_env
            )

    def test_dcgain_validation(self, transmitter, photodetector, indoor_env):
        
        indoor_env.create_envirorment(transmitter, photodetector)
        channel_model = Recursivemodel("ChannelModelA", transmitter, photodetector, indoor_env)
        channel_model.simulate_channel()
        print(channel_model)

        assert (
        channel_model._channel_dcgain[0] > 2.43e-06 and channel_model._channel_dcgain[0] < 2.44e-06 and
        channel_model._channel_dcgain[1] > 2.43e-06 and channel_model._channel_dcgain[1] < 2.44e-06 and
        channel_model._channel_dcgain[2] > 2.43e-06 and channel_model._channel_dcgain[2] < 2.44e-06
        )