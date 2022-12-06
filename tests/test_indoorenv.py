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
        "Room", size=[7.5, 5.5, 3.5], no_reflections=3, resolution=1/8
            )


def test_size(indoorenv):
    assert np.array_equal(indoorenv.size, np.array([7.5, 5.5, 3.5]))


def test_no_reflections(indoorenv):
    assert indoorenv.no_reflections == 3


def test_resolution(indoorenv):
    assert indoorenv.resolution == 1/8
