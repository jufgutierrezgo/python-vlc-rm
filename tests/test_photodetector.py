import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.photodetector import Photodetector

# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestHappyPathsRx:

    photodetector = Photodetector(
        "PD1",
        position=[6.6, 2.8, 0.8],
        normal=[0, 0, 1],
        area=1e-4,
        fov=70,
        sensor='S10917-35GT',
        idark=1e-12
            )
    
    def test_position(self):
        assert np.array_equal(self.photodetector.position, np.array([6.6, 2.8, 0.8]))

    def test_normal(self):
        assert np.array_equal(self.photodetector.normal, np.array([[0, 0, 1]]))

    def test_area(self):
        assert self.photodetector.area == 1e-4

    def test_fov(self):
        assert self.photodetector.fov == 70

    def test_sensor(self):
        assert self.photodetector.sensor == 'S10917-35GT'

    def test_idark(self):
        assert self.photodetector.idark == 1e-12
