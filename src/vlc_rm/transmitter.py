# Numeric Numpy library
import numpy as np

# Library to plot the LED patter, SPD and responsivity
import matplotlib.pyplot as plt

# Library for logging
import logging

from vlc_rm.constants import Constants as Kt


class Transmitter:
    """
    #TODO: add documentation for the class
    """

    def __init__(
        self,
        name: str,
        position: np.ndarray,
        normal: np.ndarray,
        wavelengths: np.ndarray,
        fwhm: np.ndarray,
        mlambert: float = 1,
        power: float = 1
            ) -> None:

        self._name = name
        self._position = np.array(position)
        self._normal = np.array([normal])
        self._mlambert = mlambert
        self._power = power
        self._wavelengths = np.array(wavelengths)
        self._fwhm = np.array(fwhm)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, position):
        self._position = np.array(position)
        # if self._position.size != 3:
        #    raise ValueError("Position must be a 3d-numpy array.")

    @property
    def normal(self) -> np.ndarray:
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = np.array(normal)
        if self._normal.size != 3:
            raise ValueError("Normal must be a 3d-numpy array.")

    @property
    def mlambert(self) -> float:
        return self._mlambert

    @mlambert.setter
    def mlambert(self, mlabert):
        if mlabert <= 0:
            raise ValueError("Lambert number must be greater than zero.")
        self._mlambert = mlabert

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, power):
        if power < 0:
            raise ValueError("The power must be non-negative.")
        self._power = power

    @property
    def wavelengths(self) -> np.ndarray:
        return self._wavelengths

    @wavelengths.setter
    def wavelengths(self, wavelengths):
        self._wavelengths = np.array(wavelengths)
        if self._wavelengths.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of wavelengths array must be equal to the number of LEDs.")

    @property
    def fwhm(self) -> np.ndarray:
        return self._power

    @fwhm.setter
    def fwhm(self, fwhm):
        self._fwhm = np.array(fwhm)
        if self._fwhm.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of FWHM array must be equal to the number of LEDs.")

    def __str__(self) -> str:
        return (
            f'\n List of parameters for LED transmitter: \n'
            f'Position [x y z]: {self._position} \n'
            f'Normal Vector [x y z]: {self._normal} \n'
            f'Lambert Number: {self._mlambert} \n'
            f'Power[W]: {self._power} \n'
            f'Central Wavelengths[nm]: {self._wavelengths} \n'
            f'FWHM[nm]: {self._fwhm}'
        )

    def led_pattern(self) -> None:
        """Function to create a 3d radiation pattern of the LED source.

        The LED for recurse channel model is assumed as lambertian radiator.
        The number of lambert defines the directivity of the light source.

        Parameters:
            m: Lambert number

        Returns: None.

        """

        theta, phi = np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi/2, 40)
        THETA, PHI = np.meshgrid(theta, phi)
        R = (self._mlambert + 1)/(2*np.pi)*np.cos(PHI)**self._mlambert
        X = R * np.sin(PHI) * np.cos(THETA)
        Y = R * np.sin(PHI) * np.sin(THETA)
        Z = R * np.cos(PHI)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot_surface(
            X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
            linewidth=0, antialiased=False, alpha=0.5)

        plt.show()
