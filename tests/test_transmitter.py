import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.transmitter import Transmitter

from vlc_rm.constants import Constants as Kt

# Import Numpy
import numpy as np
# Import Pytest
import pytest   


class TestHappyPathsTx:    
        
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
   
    def test_position(self):
        assert np.array_equal(self.transmitter.position, np.array([2.5, 2.5, 3]))

    def test_normal(self):
        assert np.array_equal(self.transmitter.normal, np.array([[0, 0, -1]]))

    def test_mlambert(self, transmitter):
        assert transmitter.mlambert == 1    

    def test_wavelengths(self, transmitter):
        assert np.array_equal(transmitter.wavelengths, np.array([620, 530, 475]))

    def test_fwhm(self, transmitter):
        assert np.array_equal(transmitter.fwhm, np.array([20, 45, 20]))

    def test_modulation(self, transmitter):
        assert transmitter.modulation == 'ieee16'
    
    def test_luminous_flux(self, transmitter):
        assert transmitter.luminous_flux == 5000