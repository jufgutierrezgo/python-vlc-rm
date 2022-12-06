import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.photodetector import Photodetector

# Import Numpy
import numpy as np
# Import Pytest
import pytest   

@pytest.fixture
def photodetector():
    return Photodetector(
        "PD1",
        position=[6.6, 2.8, 0.8],
        normal=[0, 0, 1],
        area=1e-4,
        fov=70,
        sensor='S10917-35GT'                
            )


def test_position(photodetector):
    assert np.array_equal(photodetector.position, np.array([6.6, 2.8, 0.8]))


def test_normal(photodetector):
    assert np.array_equal(photodetector.normal, np.array([[0, 0, 1]]))


def test_area(photodetector):
    assert photodetector.area == 1e-4


def test_fov(photodetector):
    assert photodetector.fov == 70


def test_sensor(photodetector):
    assert photodetector.sensor == 'S10917-35GT'
