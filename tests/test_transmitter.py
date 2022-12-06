# Import Module Transmitter
from vlc_rm.transmitter import Transmitter
# Import Numpy
import numpy as np
# Import Pytest
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

def test_position(transmitter):
    assert np.array_equal(transmitter.position, np.array([2, 4, 3.3]))

def test_normal(transmitter):
    assert np.array_equal(transmitter.normal, np.array([0, 0, -1]))

def test_mlambert(transmitter):
    assert transmitter.mlambert == 1

def test_power(transmitter):
    assert transmitter.power == 1

def test_wavelengths(transmitter):
    assert np.array_equal(transmitter.wavelengths, np.array([650, 530, 430, 580]))

def test_fwhm(transmitter):
    assert np.array_equal(transmitter.fwhm, np.array([20, 12, 20, 20]))