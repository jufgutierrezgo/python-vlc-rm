import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Constants Transmitter
from vlc_rm.transmitter import Transmitter
# Import Constants Photodetector
from vlc_rm.photodetector import Photodetector
# Import Constants Photodetecto
from vlc_rm.indoorenv import Indoorenv


# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestHappyPathsEnv:

    indoorenv = Indoorenv(
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

    def test_size(self):
        assert np.array_equal(self.indoorenv.size, np.array([5, 5, 3]))

    def test_no_reflections(self):
        assert self.indoorenv.no_reflections == 3

    def test_resolution(self):
        assert self.indoorenv.resolution == 1/8

    def test_ceiling(self):
        assert np.array_equal(self.indoorenv.ceiling, np.array([0.8, 0.8, 0.8]))

    def test_west(self):
        assert np.array_equal(self.indoorenv.west, np.array([0.8, 0.8, 0.8]))

    def test_north(self):
        assert np.array_equal(self.indoorenv.north, np.array([0.8, 0.8, 0.8]))

    def test_east(self):
        assert np.array_equal(self.indoorenv.east, np.array([0.8, 0.8, 0.8]))

    def test_south(self):
        assert np.array_equal(self.indoorenv.south, np.array([0.8, 0.8, 0.8]))

    def test_floor(self):
        assert np.array_equal(self.indoorenv.floor, np.array([0.3, 0.3, 0.3]))
