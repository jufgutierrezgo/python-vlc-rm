import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.transmitter import Transmitter

from vlc_rm.constants import Constants as Kt

# Import Numpy
import numpy as np
# Import Pytest
import pytest   


class TestTransmitter:    

    POSITION = [2.5, 2.5, 3]
    NORMAL = [0, 0, -1]
    MLAMBERT = 1
    WAVELENGTHS = [620, 530, 475]
    FWHM = [20, 45, 20]
    MODULATION = 'ieee16'
    LUMINOUS_FLUX = 5000

    transmitter = Transmitter(
        "Led1",
        position=POSITION,
        normal=NORMAL,
        mlambert=MLAMBERT,
        wavelengths=WAVELENGTHS,
        fwhm=FWHM,
        modulation=MODULATION,
        luminous_flux=LUMINOUS_FLUX
                )
   
    def test_position(self):
        assert np.array_equal(self.transmitter.position, np.array(self.POSITION))

    def test_normal(self):
        assert np.array_equal(self.transmitter.normal, np.array([self.NORMAL]))

    def test_mlambert(self):
        assert self.transmitter.mlambert == self.MLAMBERT

    def test_wavelengths(self):
        assert np.array_equal(self.transmitter.wavelengths, np.array(self.WAVELENGTHS))

    def test_fwhm(self):
        assert np.array_equal(self.transmitter.fwhm, np.array(self.FWHM))

    def test_modulation(self):
        assert self.transmitter.modulation == self.MODULATION
    
    def test_luminous_flux(self):
        assert self.transmitter.luminous_flux == self.LUMINOUS_FLUX

    def test_position_error(self):        
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=['a', 2, 3],
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=[2.5, 2.5, 3, 4],
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
    
    def test_normal_error(self):        
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=['a', 0, -1],
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=[0, 0, 1, 1],
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )

    def test_mlambert_error(self):        
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert='a',
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=-1,
                wavelengths=self.WAVELENGTHS,
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
    
    def test_wavelengths_error(self):   
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=['a', 550, 680],
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=[550, 680],
                fwhm=self.FWHM,
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
            
    def test_fwhm_error(self):   
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=['a', 10, 20],
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[10, 20],
                modulation=self.MODULATION,
                luminous_flux=self.LUMINOUS_FLUX
                        )
    
    def test_modulation_error(self):
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[20, 10, 20],
                modulation='okk',
                luminous_flux=self.LUMINOUS_FLUX
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[20, 10, 20],
                modulation='csk',
                luminous_flux=self.LUMINOUS_FLUX
                        )

    def test_luminous_flux_error(self):
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[20, 10, 20],
                modulation='ieee16',
                luminous_flux=-10
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[20, 10, 20],
                modulation='ieee16',
                luminous_flux=0
                        )
        with pytest.raises(ValueError):
            transmitter = Transmitter(
                "Led1",
                position=self.POSITION,
                normal=self.NORMAL,
                mlambert=self.MLAMBERT,
                wavelengths=self.WAVELENGTHS,
                fwhm=[20, 10, 20],
                modulation='ieee16',
                luminous_flux='a'
                        )