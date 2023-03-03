import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.photodetector import Photodetector

# Import Numpy
import numpy as np
# Import Pytest
import pytest


class TestPhotodetector:

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
        assert np.array_equal(
            self.photodetector.position,
            np.array(self.POSITION, dtype=np.float32)
            )

    def test_normal(self):
        assert np.array_equal(self.photodetector.normal, np.array([self.NORMAL]))

    def test_area(self):
        assert self.photodetector.area == np.float32(self.AREA)

    def test_fov(self):
        assert self.photodetector.fov == self.FOV

    def test_sensor(self):
        assert self.photodetector.sensor == self.SENSOR

    def test_idark(self):
        assert self.photodetector.idark == self.IDARK

    def test_position_error(self):        
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=[0, 1],
                normal=self.NORMAL,
                area=self.AREA,
                fov=self.FOV,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=['a', 0.5, 0],
                normal=self.NORMAL,
                area=self.AREA,
                fov=self.FOV,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
            
    def test_normal_error(self):        
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=self.POSITION,
                normal=[0, 0],
                area=self.AREA,
                fov=self.FOV,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=self.POSITION,
                normal=['a', 0, 0],
                area=self.AREA,
                fov=self.FOV,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
    
    def test_fov_error(self):
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=self.POSITION,
                normal=self.NORMAL,
                area=self.AREA,
                fov='a',
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=self.POSITION,
                normal=self.NORMAL,
                area=self.AREA,
                fov=-5,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )
        with pytest.raises(ValueError):
            photodetector = Photodetector(
                "PD1",
                position=self.POSITION,
                normal=self.NORMAL,
                area=self.AREA,
                fov=91,
                sensor=self.SENSOR,
                idark=self.IDARK
                    )