import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Constants Transmitter
from vlc_rm.transmitter import Transmitter
# Import Constants Photodetector
from vlc_rm.photodetector import Photodetector
# Import Constants Photodetecto
from vlc_rm.indoorenv import Indoorenv
# Import Constants Photodetector
from vlc_rm.recursivemodel import Recursivemodel

# Import Numpy
import numpy as np
# Import Pytest
import pytest   

@pytest.fixture
def indoorenv():
    return Indoorenv(
        "Room",
        size=[5, 5, 3],
        no_reflections=3,
        resolution=1/8,
        ceiling=[0.8, 0.8, 0.8, 0.8],
        west=[0.8, 0.8, 0.8, 0.8],
        north=[0.8, 0.8, 0.8, 0.8],
        east=[0.8, 0.8, 0.8, 0.8],
        south=[0.8, 0.8, 0.8, 0.8],
        floor=[0.3, 0.3, 0.3, 0.3]
            )


def test_size(indoorenv):
    assert np.array_equal(indoorenv.size, np.array([5, 5, 3]))


def test_no_reflections(indoorenv):
    assert indoorenv.no_reflections == 3


def test_resolution(indoorenv):
    assert indoorenv.resolution == 1/8


def test_ceiling(indoorenv):
    assert np.array_equal(indoorenv.ceiling, np.array([0.8, 0.8, 0.8, 0.8]))


def test_west(indoorenv):
    assert np.array_equal(indoorenv.west, np.array([0.8, 0.8, 0.8, 0.8]))


def test_north(indoorenv):
    assert np.array_equal(indoorenv.north, np.array([0.8, 0.8, 0.8, 0.8]))


def test_east(indoorenv):
    print(indoorenv.east)
    assert np.array_equal(indoorenv.east, np.array([0.8, 0.8, 0.8, 0.8]))


def test_south(indoorenv):
    assert np.array_equal(indoorenv.south, np.array([0.8, 0.8, 0.8, 0.8]))


def test_floor(indoorenv):
    assert np.array_equal(indoorenv.floor, np.array([0.3, 0.3, 0.3, 0.3]))
