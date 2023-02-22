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

    DIST_COSINE = np.array([[
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01, 
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00],
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00]],
            [
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 0.0000e+00, 7.0711e-01, 1.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00, 7.0711e-01,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [7.0711e-01, 7.0711e-01, 1.0000e+00, 7.0711e-01, 0.0000e+00,
                7.0711e-01, 7.0711e-01, 7.0711e-01],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00],
            [0.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                1.0000e+00, 0.0000e+00, 1.0000e+00],
            [1.0000e+00, 7.0711e-01, 7.0711e-01, 7.0711e-01, 7.0711e-01,
                0.0000e+00, 1.0000e+00, 0.0000e+00]
            ]
        ],
        dtype=np.float32)

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

    def test_parameters(self):
        
        led1 = Transmitter(
            "Led1",
            position=[0.5, 0.5, 1],
            normal=[0, 0, -1],
            mlambert=1,
            wavelengths=[620, 530, 475],
            fwhm=[20, 45, 20],
            modulation='ieee16',
            luminous_flux=5000
                    )  

        pd1 = Photodetector(
            "PD1",
            position=[0.5, 0.5, 0],
            normal=[0, 0, 1],
            area=(1e-4),
            # area=0.5e-4,
            fov=85,
            sensor='S10917-35GT',
            idark=1e-12
                    )

        basic_env = Indoorenv(
            "Basic-Env",
            size=[1, 1, 1],
            no_reflections=3,
            resolution=1,
            ceiling=[1, 1, 1],
            west=[1, 1, 1],
            north=[1, 1, 1],
            east=[1, 1, 1],
            south=[1, 1, 1],
            floor=[1, 1, 1]
                )

        basic_env.create_envirorment(led1, pd1)
        print(repr(basic_env.wall_parameters))
        
        assert np.allclose(
            basic_env.wall_parameters,
            self.DIST_COSINE
        )
                
            
        
