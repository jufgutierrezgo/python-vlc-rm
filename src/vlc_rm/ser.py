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

    def _create_symbols(self) -> None:       
        """
        This function creates the symbols array to transmit.
        """
        # create a random symbols identifier (decimal) for payload
        self._symbols_decimal = np.random.randint(
                0,
                self._order_csk-1,
                (self._no_symbols),
                dtype='int16'
            )

        self._symbols_payload = np.zeros((Kt.NO_LEDS, self._no_symbols))

        # using symbols identifier numbers to define the CSK symbols
        for index, counter in zip(self._symbols_decimal, range(self._no_symbols)):
            self._symbols_payload[:, counter] = Kt.IEEE_16CSK[:, index]


        # Define the number of symbols for delimiter header
        self._delimiter_set = 3

        # add to the payload three base-set of symbols
        self._symbols_csk = np.concatenate((
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                np.identity(Kt.NO_LEDS),
                self._symbols_payload),
                axis=1
            )

    def _transmit_symbols(self) -> None:       
        """ This function computes the channel transformation of the
        original symbols.
        """

        self._symbols_transmitted = np.matmul(
            np.matmul(
                self._recursivemodel.channelmatrix,
                self._iler_matrix
                ),
            self._symbols_csk
            )

    def _add_noise(self, target_snr_db) -> None:
        """ 
        This function adds AWGN noise to the self._symbols_transmitted
        array.
        """

        plt.stem(self._symbols_transmitted[0, :])
        plt.show()

        # Create an empty numpy-array equal to self._symbols_transmitted
        self._noise_symbols = np.empty_like(self._symbols_transmitted)

        for color_channel in range(Kt.NO_DETECTORS):
            # define the x_current signal to add AWGN 
            x_current = self._symbols_transmitted[color_channel, :]
            # Calculate the power of the signal in the color channel
            x_watts = x_current ** 2
            # Calculate signal power and convert to dB 
            sig_avg_watts = np.mean(x_watts)
            sig_avg_db = 10 * np.log10(sig_avg_watts)
            # Calculate noise according to [2] then convert to watts
            noise_avg_db = sig_avg_db - target_snr_db
            noise_avg_watts = 10 ** (noise_avg_db / 10)
            # Generate an sample of white noise
            mean_noise = 0        
            noise_current = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))
            # Noise up the original signal
            signal_noise = x_current + noise_current
            # Convert negative values to zero
            signal_noise[signal_noise < 0] = 0
            # Save signal with noise in array
            self._noise_symbols[color_channel, :] = signal_noise


    def _decode_symbols(self):
        """
        This funtion decodes the CSK symbols from the self._noise_symbols
        """

        # get the header and payload of the noisy received symbols
        self._rx_header = self._noise_symbols[:, 0:Kt.NO_DETECTORS*self._delimiter_set]
        self._rx_payload = self._noise_symbols[:, Kt.NO_DETECTORS*self._delimiter_set-1:-1]

        # split the header into base-set
        self.bases_split = np.array(
            np.array_split(
                self._rx_header,
                self._delimiter_set,
                axis=1
                )
            )

        # average of the base-sets
        self.avg_bases = np.mean(
            self.bases_split,
            axis=0
            )
        
        # computes the inverse channel matrix from transmitted header
        self._rx_channel_inverse = np.linalg.inv(self.avg_bases)

        # Apply the inverse matrix for decoding
        self._inverse_rx_symbols = np.matmul(
                self._rx_channel_inverse,
                self._rx_payload
            )
        
    def __str__(self) -> str:
        return (
            f'\n List of parameter of SER object \n'
            f'Inverse LER Matrix: \n {self._iler_matrix} \n'
        )
