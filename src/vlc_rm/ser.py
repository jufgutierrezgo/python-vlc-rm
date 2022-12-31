import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.constants import Constants as Kt

from vlc_rm.transmitter import Transmitter

from vlc_rm.photodetector import Photodetector

from vlc_rm.indoorenv import Indoorenv

from vlc_rm.recursivemodel import Recursivemodel

from vlc_rm.loader import Loader

import luxpy as lx

# Numeric Numpy library
import numpy as np

# Library to plot the LED patter, SPD and responsivity
import matplotlib.pyplot as plt

import logging


class SymbolErrorRate:
    """
    This class defines the transmitter features
    """

    def __init__(
        self,
        name: str,
        recursivemodel: Recursivemodel,
        order_csk: int,
        no_symbols: int
            ) -> None:

        self._order_csk = int(order_csk)
        #if (self._order_csk & (self._order_csk-1) == 0) and (self._order_csk != 0):
        #    raise ValueError(
        #        "Resolution of points must be a real integer between 0 and 10.")
        
        self._no_symbols = int(no_symbols)
        if self._no_symbols <= 0:
            raise ValueError(
                "No. of symbols must be greater than zero.")

        self._recursivemodel = recursivemodel
        if not type(self._recursivemodel) is Recursivemodel:
            raise ValueError(
                "Recursivemodel attribute must be an object type Recursivemodel.")

        @property
        def order_csk(self) -> int:
            """The number of symbols in the constellations"""
            return self._order_csk

        @order_csk.setter
        def order_csk(self, order_csk):
            self._order_csk = order_csk
            if (self._order_csk & (self._order_csk-1) == 0) and (self._order_csk != 0):
                raise ValueError(
                    "Resolution of points must be a real integer between 0 and 10.")

        @property
        def no_symbols(self) -> int:
            """The number of symbols for the transmission"""
            return self._no_symbols

        @no_symbols.setter
        def order_csk(self, no_symbols):
            self._no_symbols = no_symbols
            if self._no_symbols <= 0:
                raise ValueError(
                    "Number of symbols must be greater than zero.")

    def _compute_iler(self) -> None:
        """
        This function computes the inverse luminous efficacy radiation (LER) matrix.
        This matrix has a size of NO_LEDS x NO_LEDS
        """
        self._iler_matrix = np.zeros((Kt.NO_LEDS, Kt.NO_LEDS))

        for i in range(Kt.NO_LEDS):
            self._iler_matrix[i, i] = 1/lx.spd_to_ler(
                np.vstack(
                    [
                        self._recursivemodel.wavelenght,
                        self._recursivemodel._spd_data[:, i]
                    ])
                )

    def _create_symbols(self):       
        """
        This function creates the symbols array to transmit.
        """
        self._symbols_decimal = np.random.randint(
                0,
                self._order_csk-1,
                (self._no_symbols),
                dtype='int16'
            )

        self._symbols_payload = np.zeros((Kt.NO_LEDS, self._no_symbols))

        for index, counter in zip(self._symbols_decimal, range(self._no_symbols)):
            self._symbols_payload[:, counter] = Kt.IEEE_16CSK[:, index]
        
        # add to the payload three base symbols
        self._symbols_csk = np.concatenate((
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                self._symbols_payload),
                axis=1
            )

    def _transmit_symbols(self):       
        """
        This function computes the channel transformation of the origial 
        symbols.
        """

        self._symbols_transmitted = np.matmul(
            np.matmul(
                self._recursivemodel.channelmatrix,
                self._iler_matrix
                ),
            self._symbols_csk
            )

    def __str__(self) -> str:
        return (
            f'\n List of parameter of SER object \n'
            f'Inverse LER Matrix: \n {self._iler_matrix} \n'
        )
