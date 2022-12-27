import numpy as np
from numpy.core.function_base import linspace

from scipy import stats

import matplotlib.pyplot as plt

import luxpy as lx

import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

from vlc_rm.constants import Constants as Kt

from vlc_rm.transmitter import Transmitter

from vlc_rm.photodetector import Photodetector

from vlc_rm.indoorenv import Indoorenv

from vlc_rm.loader import Loader


class Recursivemodel:
    """
        This class contains the function to calculates the CIR and
        DC-gain in the optical channel and lighting parameters
    """

    def __init__(
        self,
        name: str,
        led: Transmitter,
        photodetector: Photodetector,
        room: Indoorenv
            ) -> None:

        self.name = name

        self._led = led
        if not type(self._led) is Transmitter:
            raise ValueError(
                "Tranmistter attribute must be an object type Transmitter.")

        self._photodetector = photodetector
        if not type(photodetector) is Photodetector:
            raise ValueError(
                "Receiver attribute must be an object type Photodetector.")

        self._room = room
        if not type(self._room) is Indoorenv:
            raise ValueError(
                "Indoor environment attribute must be an object type IndoorEnv.")

        self._channel_dcgain = np.zeros((1, Kt.NO_LEDS))
        self._channelmatrix = np.zeros(
            (Kt.NO_DETECTORS, Kt.NO_LEDS),
            dtype=np.float32
            )
        self._illuminance = 0
        self._cri = 0
        self._cct = 0

    @property
    def channel_dcgain(self):
        return self._channel_dcgain

    @property
    def channelmatrix(self):
        return self._channelmatrix

    @property
    def illuminance(self):
        return self._illuminance

    @property
    def cri(self):
        return self._cri

    @property
    def cct(self):
        return self._cct

    def __str__(self) -> str:
        return (
            f'\n|=============== Simulation results ================|\n'
            f'DC-Gain [w]: \n {self._channel_dcgain} \n'
            f'Crosstalk Matrix: \n{self._channelmatrix} \n'
            f'Illuminance [lx]: {self._illuminance} \n'
            f'CCT: {self._cct} \n'
            f'CRI: {self._cri} \n'
        )

    def simulate_channel(self) -> None:
        """ 
        This method simulates the indoor enviornment
        """

        loader = Loader(
            "Simulating indoor environment ...", "Simulation done!", 0.05
            ).start()

        self._compute_cir()
        self._compute_dcgain()
        self._create_spd()
        self._compute_cct_cri()
        self._compute_irradiance()
        self._compute_illuminance()
        self._compute_channelmatrix()

        loader.stop()

    def _compute_cir(self) -> None:
        """ Function to compute the channel impulse response
            for each reflection.

        Parameters:
            led.m: lambertian number to tx emission
            led.wall_parameters: 3D array with distance and
                cosine pairwise-elemets.
            pd.area: sensitive area in photodetector


        Returns: A list with 2d-array [power_ray,time_delay] collection
            for each refletion [h_0,h_1,...,h_k].

        """

        # defing variables and arrays
        tx_index_point = self._room.no_points-2
        rx_index_point = self._room.no_points-1

        cos_phi = np.zeros(
            (self._room.no_points), dtype=np.float16)
        dis2 = np.zeros((
            self._room.no_points, self._room.no_points), dtype=np.float16)

        h0_se = np.zeros((self._room.no_points, Kt.NO_LEDS), dtype=np.float64)
        h0_er = np.zeros((self._room.no_points, 1), dtype=np.float64)

        # Time delay between source and each cells
        # h0_se[:,1] = room.wall_parameters[0,tx_index_point,:]/SPEED_OF_LIGHT
        # Time delay between receiver and each cells
        # h0_er[:,1] = room.wall_parameters[0,rx_index_point,:]/SPEED_OF_LIGHT

        # define distance^2 and cos_phi arrays
        dis2 = np.power(self._room.wall_parameters[0, :, :], 2)
        cos_phi = self._room.wall_parameters[1, int(tx_index_point), :]

        # computing the received power by each smaller area from light sooure
        tx_power = (
            (self._led.mlambert+1)/(2*np.pi) *
            np.multiply(
                np.divide(
                    1,
                    dis2[tx_index_point, :],
                    out=np.zeros((self._room.no_points)),
                    where=dis2[tx_index_point, :] != 0),
                np.power(cos_phi, self._led.mlambert)
                    )
                )

        rx_wall_factor = (
            self._photodetector.area *
            self._room.wall_parameters[1, int(rx_index_point), :]
            )

        # Differential power between all grid points without reflectance
        dP_ij = np.zeros(
            (self._room.no_points, self._room.no_points), np.float32)
        dP_ij = (
            np.divide(
                self._room.deltaA*self._room.wall_parameters[1, :, :] *
                np.transpose(self._room.wall_parameters[1, :, :]),
                np.pi * dis2, out=np.zeros_like(dP_ij),
                where=dis2 != 0
                )
            )

        # Array creation for dc_gain and previuos dc_gain
        self.h_k = []
        hlast_er = []

        # Array creation for time delay
        self.delay_hk = []
        delay_hlast_er = []

        # Time delay matrix
        tDelay_ij = np.zeros(
            (self._room.no_points, self._room.no_points), dtype=np.float32)
        tDelay_ij = self._room.wall_parameters[0, :, :]/Kt.SPEED_OF_LIGHT
        # print(np.shape(tDelay_ij))

        # TODO: check whether you can replace this for by vectorized
        # operations or comprehension operations
        for i in range(self._room.no_reflections+1):

            # Creates the array to save h_k reflections response
            # and last h_er response
            self.h_k.append(np.zeros((self._room.no_points, Kt.NO_LEDS), np.float32))
            hlast_er.append(np.zeros((self._room.no_points, Kt.NO_LEDS), np.float32))

            # Creates the array to save time-delay reflections
            # response and last h_er
            self.delay_hk.append(np.zeros(
                (self._room.no_points, 1), np.float32))
            delay_hlast_er.append(np.zeros(
                (self._room.no_points, 1), np.float32))

            if i == 0:

                # Magnitude of CIR in LoS
                self.h_k[i][0, :] = (
                    tx_power[int(rx_index_point)] *
                    rx_wall_factor[int(tx_index_point)]
                    )

                # Time Delay of CIR in LoS
                self.delay_hk[i][0, 0] = tDelay_ij[
                    int(tx_index_point), int(rx_index_point)
                        ]

            elif i == 1:
                # Impulse response between source and each cells without
                # reflectance. The reflectance is added in the h_k computing.
                h0_se = np.multiply(
                    np.reshape(
                        np.multiply(
                            self._room.deltaA * tx_power,
                            self._room.wall_parameters[
                                1, :, int(tx_index_point)]
                                ),
                        (-1, 1)
                            ),
                    self._room.reflectance_vectors
                    )

                # Impulse response between receiver and each cells
                h0_er[:, 0] = np.divide(
                    np.multiply(
                        self._room.wall_parameters[1, :, int(rx_index_point)],
                        rx_wall_factor),
                    np.pi*dis2[rx_index_point, :],
                    out=np.zeros((self._room.no_points)),
                    where=dis2[rx_index_point, :] != 0
                            )

                # print("h0_se array->:",h0_se[:,0])
                # print("h0_er array->:",h0_er[:,0])

                # Previous h_er RGBY vectors of magnitude for LoS
                hlast_er[i] = np.repeat(h0_er, repeats=Kt.NO_LEDS, axis=1)

                # Current vector for h1 impulse response for RGBY
                # Red-Green-Blue-Yellow
                self.h_k[i] = np.multiply(h0_se, hlast_er[i])

                # Time-Delay computing
                delay_hlast_er[i] = tDelay_ij[int(rx_index_point), :]
                self.delay_hk[i] = tDelay_ij[
                    int(tx_index_point), :] + delay_hlast_er[i]

                # np.savetxt(CIR_PATH+"h1.csv", h_k[i], delimiter=","

            elif i >= 2:

                # Time-Delay computing
                delay_hlast_er[i] = np.sum(
                    np.reshape(delay_hlast_er[i-1], (1, -1)) + tDelay_ij,
                    axis=1)/self._room.no_points

                self.delay_hk[i] = tDelay_ij[
                    int(tx_index_point), :] + delay_hlast_er[i]

                # Computes the last h_er to compute h_k
                for color in range(Kt.NO_LEDS):

                    hlast_er[i][:, color] = np.sum(
                        np.multiply(
                            hlast_er[i-1][:, color],
                            np.multiply(
                                self._room.reflectance_vectors[:, color], dP_ij)
                            ),
                        axis=1
                        )

                    self.h_k[i][:, color] = np.multiply(
                        h0_se[:, 0], hlast_er[i][:, color])
                    # print("h_k->",np.shape(self.h_k[i]))

    def _compute_dcgain(self) -> None:
        """
        This function calculates the total power received
        from LoS and h_k reflections
        """

        self.h_dcgain = np.zeros((self._room.no_reflections+1, Kt.NO_LEDS), np.float32)

        for i in range(0, self._room.no_reflections+1):
            self.h_dcgain[i, :] = np.sum(self.h_k[i][0:-2, 0:Kt.NO_LEDS], axis=0)

        self._channel_dcgain = np.sum(self.h_dcgain, axis=0)

    def print_Hk(self) -> None:
        """
        This function calculates the DC-Gain for each reflection.
        """
        for i in range(0, self._room.no_reflections+1):
            print("\n DC-gain for H{} response [W]:\n {}".format(i, self.h_dcgain[i, :]))

    def _create_histograms(self) -> None:
        """Function to create histograms from channel impulse
        response raw data.

        The channel impulse response raw data is a list with power and
        time delay of every ray. Many power histograms are created
        based on time resolution defined in the TIME_RESOLUTION constant.

        Parameters:
            h_k: list with channel impulse response [h_0,h_1,...,h_k].
            k_reflec: number of reflections
            no_cells: number of points of model

        Returns: A List with the next parameters
            hist_power_time: Power histograms for each reflection
            total_ht: total power CIR histrogram
            time_scale: 1d-array with time scale

        """

        self.time_resolution = 0.2e-9
        self.bins_hist = 300

        self.total_histogram = np.zeros((self.bins_hist, 4))
        self.hist_power_time = []
        delay_aux = np.zeros((self._room.no_points, 1))

        #TODO: required?
        print("//------------- Data report ------------------//")
        print("Time resolution [s]:"+str(self.time_resolution))
        print("Number of Bins:"+str(self.bins_hist))

        delay_los = self.delay_hk[0][0, 0]

        print("Optical power reported in histograms:")

        for k_reflec in range(self._room.no_reflections+1):

            self.hist_power_time.append(
                np.zeros((self.bins_hist, Kt.NO_LEDS), np.float32))

            # Delay_aux variable
            delay_aux = np.reshape(
                self.delay_hk[k_reflec], (-1, 1)) - delay_los

            delay_aux = np.floor(delay_aux/self.time_resolution)
            # print(np.shape(delay_aux))

            for j in range(self._room.no_points):
                self.hist_power_time[k_reflec][int(delay_aux[j, 0]), :] += self.h_k[k_reflec][j, :]

            self.time_scale = linspace(
                0,
                self.bins_hist * self.time_resolution,
                num=self.bins_hist
                )
            print(
                "H" + str(k_reflec) + ": ",
                np.sum(self.hist_power_time[k_reflec], axis=0)
                )

            self.total_histogram += self.hist_power_time[k_reflec]

    def _plot_cir(self, channel: str = "") -> None:
        """
        This function plots the channel impulse response for 4 colors  
        """    
        self.channel = channel

        if self.channel == 'red':
            color_number = 0
        elif self.channel == 'green':
            color_number = 1
        elif self.channel == 'blue':
            color_number = 2
        elif self.channel == 'yellow':
            color_number = 3
        else:
            #TODO: better throw an exception
            print(
                "Invalid color name ('red' or 'green' or 'blue' or 'yellow').")
            color_number = -1

        if color_number == -1:
            #TODO: remove, refactor
            print("Graphs were not generated.")
        else:
            for k_reflec in range(0, self._room.no_reflections+1):

                fig, (vax) = plt.subplots(1, 1, figsize=(12, 6))

                vax.plot(
                    self.time_scale,
                    self.hist_power_time[k_reflec][:, color_number],
                    'o',
                    markersize=2
                    )
                vax.vlines(
                    self.time_scale,
                    [0],
                    self.hist_power_time[k_reflec][:, color_number],
                    linewidth=1
                    )

                vax.set_xlabel("time(s) \n Time resolution:", fontsize=15)
                vax.set_ylabel('Power(W)', fontsize=15)
                vax.set_title(
                    "Channel "+self.channel
                    + " Impulse Response h"
                    + str(k_reflec)
                    + "(t)",
                    fontsize=20
                    )

                vax.grid(color='black', linestyle='--', linewidth=0.5)

                fig.savefig(Kt.REPORT_PATH+"h"+str(k_reflec)+".png")
                plt.show()

            fig, (vax) = plt.subplots(1, 1, figsize=(12, 6))

            vax.plot(
                self.time_scale, self.total_histogram[:, color_number],
                'o',
                markersize=2
                )
            vax.vlines(
                self.time_scale,
                [0],
                self.total_histogram[:, color_number],
                linewidth=1
                )

            vax.set_xlabel("time(s) \n Time resolution:", fontsize=15)
            vax.set_ylabel('Power(W)', fontsize=15)
            vax.set_title(
                "Channel "+self.channel+" Total Impulse Response h(t)",
                fontsize=20
                )

            vax.grid(color='black', linestyle='--', linewidth=0.5)

            fig.savefig(Kt.REPORT_PATH+self.channel+"-htotal.png")
            plt.show()

    def _create_spd(self) -> None:
        """
        This function creates a SPD of LED from central wavelengths,
        FWHM and DC gain of channel
        """

        # Array for wavelenght points from 380nm to (782-2)nm with 2nm steps
        self.wavelenght = np.arange(380, 782, 2)

        # Numpy Array to save the spectral power distribution of each color channel
        self._spd_data = np.zeros((self.wavelenght.size, Kt.NO_LEDS))

        for i in range(Kt.NO_LEDS):
            # Arrays to estimate the RGBY gain spectrum
            self._spd_data[:, i] = self._channel_dcgain[i]*stats.norm.pdf(
                self.wavelenght, self._led._wavelengths[i], self._led._fwhm[i]/2)

        self._spd_total = np.sum(self._spd_data, axis=1)

    def _plot_spd(self) -> None:
        """ This function plots the SPD of QLED """
        # plot red spd data
        for i in range(Kt.NO_LEDS):
            plt.plot(self.wavelenght, self._spd_data[:, i])
        
        plt.title("Spectral Power distribution of QLED")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Radiometric Power [W]")
        plt.grid()
        plt.show()

    def _compute_cct_cri(self) -> None:
        """ This function calculates a CCT and CRI of the QLED SPD."""

        # Computing the xyz coordinates from SPD-RGBY estimated spectrum
        xyz = lx.spd_to_xyz(
            [
                self.wavelenght,
                self._spd_total
            ])
        # Computing the CRI coordinates from SPD-RGBY estimated spectrum
        self._cri = lx.cri.spd_to_cri(
            np.vstack(
                    [
                        self.wavelenght,
                        self._spd_total/self._photodetector.area
                    ]
                )
            )
        # Computing the CCT coordinates from SPD-RGBY estimated spectrum
        self._cct = lx.xyz_to_cct_ohno2014(xyz)

    def _compute_irradiance(self) -> None:
        """ This function calculates the irradiance."""
        
        self._irradiance = lx.spd_to_power(
            np.vstack(
                [self.wavelenght, self._spd_total/self._photodetector.area]
                    ),
            ptype='ru'
            )
    
    def _compute_illuminance(self) -> None:
        """ This function calculates the illuminance."""
        self._illuminance = lx.spd_to_power(
            np.vstack(
                [self.wavelenght, self._spd_total/self._photodetector.area]
                        ),
            ptype='pu'
            )

    def _compute_channelmatrix(self) -> None:
        """ This function computes channel matrix."""

        for j in range(Kt.NO_LEDS):
            for i in range(Kt.NO_DETECTORS):
                self._channelmatrix[i][j] = np.dot(
                    self._spd_data[:, j], self._photodetector.responsivity[:, i])
