import numpy as np
import matplotlib.pyplot as plt
from vlc_rm.constants import Constants as Kt


class Photodetector:
    """
    This class defines the photodetector features

    """

    def __init__(
        self,
        name: str,
        position: np.ndarray,
        normal: np.ndarray,
        area: np.ndarray,
        sensor: str = " ",
        fov: float = 90
    ) -> None:

        self._name = name
        self._position = np.array(position)
        self._normal = np.array([normal])
        self._area = np.array(area)
        self._fov = fov
        self._sensor = sensor

        if self.sensor == 'TCS3103-04':
            # read text file into NumPy array
            self.responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityTCS3103-04.txt")  # TODO: these files should be on a data directory
            print("Responsivity loaded succesfully")
        elif self.sensor == 'S10917-35GT':
            self.responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityS10917-35GT.txt")
            print("Responsivity loaded succesfully")
        elif self.sensor == ' ':
            print("Specify sensor reference")
        else:
            print("Sensor reference not valid")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def normal(self) -> np.ndarray:
        return self._normal

    @normal.setter
    def position(self, normal):
        self._normal = np.array(normal)

    @property
    def area(self) -> float:
        return self._area

    @area.setter
    def area(self, area):
        self._area = area

    @property
    def fov(self) -> float:
        return self._fov

    @fov.setter
    def fov(self, fov):
        self._fov = fov

    @property
    def sensor(self) -> str:
        return self._sensor

    @sensor.setter
    def sensor(self, sensor) -> None:
        self._sensor = sensor

        if self.sensor == 'TCS3103-04':
            self.responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityTCS3103-04.txt")
            print("Responsivity loaded succesfully")
        elif self.sensor == 'S10917-35GT':
            self.responsivity = np.loadtxt(
                Kt.SENSOR_PATH+"ResponsivityS10917-35GT.txt")
        else:
            raise ValueError(f"Unknown value {sensor}")

    def __str__(self) -> str:
        return (
            f'\n List of parameters for photodetector: \n'
            f'Position [x y z]: {self._position} \n'
            f'Normal Vector [x y z]: {self._normal} \n'
            f'Active Area[m2]: {self._area} \n'
            f'FOV: {self._fov} \n'
            f'Sensor: {self._sensor}'
        )

    def plot_responsivity(self) -> None:
        plt.plot(
            self.responsivity[:, 0],
            self.responsivity[:, 1],
            color='r',
            linestyle='dashed'
        )
        plt.plot(
            self.responsivity[:, 0],
            self.responsivity[:, 2],
            color='g',
            linestyle='dashed'
        )
        plt.plot(
            self.responsivity[:, 0],
            self.responsivity[:, 3],
            color='b',
            linestyle='dashed'
        )
        plt.title("Spectral Responsiity of Photodetector")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Responsivity [A/W]")
        plt.grid()
        plt.show()
