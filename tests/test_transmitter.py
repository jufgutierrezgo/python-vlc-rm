# Import Module Transmitter
from vlc_rm.transmitter import Transmitter
# Import Numpy
import numpy as np

import pytest   

@pytest.fixture
def transmitter():
    return Transmitter(
    "Led1",
    position=[2, 4, 3.3],
    normal=[0, 0, -1],
    mlambert=1,
    power=1,
    wavelengths=[650, 530, 430, 580],
    fwhm=[20, 12, 20, 20]
                )
    return led

def test_position(transmitter):
    assert np.array_equal(transmitter.position, np.array([2, 4]))
