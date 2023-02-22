import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.photodetector import Photodetector

# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestHappyPathsRx:

    POSITION = [6.6, 2.8, 0.8]
    NORMAL = [0, 0, 1]
    AREA = 1e-4
    FOV = 70
    SENSOR = 'S10917-35GT'
    IDARK = 1e-12

    photodetector = Photodetector(
        "PD1",
        position=POSITION,
        normal=NORMAL,
        area=AREA,
        fov=FOV,
        sensor=SENSOR,
        idark=IDARK
            )
    
    def test_position(self):
        assert np.array_equal(self.photodetector.position, np.array(self.POSITION))

    def test_normal(self):
        assert np.array_equal(self.photodetector.normal, np.array([self.NORMAL]))

    def test_area(self):
        assert self.photodetector.area == self.AREA

    def test_fov(self):
        assert self.photodetector.fov == self.FOV

    def test_sensor(self):
        assert self.photodetector.sensor == self.SENSOR

    def test_idark(self):
        assert self.photodetector.idark == self.IDARK
