from vlc_rm.constants import Constants as Kt

# Numeric Numpy library
import numpy as np
# Library to plot SPD and responsivity
import matplotlib.pyplot as plt
# Library to compute color and photometry parameters
import luxpy as lx


class Transmitter:
    """
    This class defines the transmitter features
    """

    
    def __init__(
        self,
        name: str = "LED",
        led_type: str = "gaussian",
        reference: str = "None",
        position: np.ndarray = [1, 1, 1],
        normal: np.ndarray = [0, -1, 0],
        wavelengths: np.ndarray=[400, 500, 600],
        fwhm: np.ndarray=[10, 10, 10],
        mlambert: float = 1,        
        constellation: str = 'ieee16',
        luminous_flux: float = 1
            ) -> None:

        self._name = name

        if isinstance(led_type, str):
            self._led_type = led_type
            if self._led_type == 'custom':
                if isinstance(reference, str):
                    self._reference = reference                
                    if self._reference == 'RGB-Phosphor':                            
                        self._rgb_led_spectrum = np.loadtxt(
                            Kt.LED_PATH+"rgb-phosphor-spectrum.txt")
                    else: 
                        raise ValueError("reference must be 'RGB-Phosphor'")
                else:
                    raise ValueError("reference must be a string")
            elif self._led_type == 'gaussian':
                pass
            else:
                raise ValueError("type must be string either 'gaussian' or 'custom'")    
        else:
            raise ValueError("type must be string either 'gaussian' or 'custom'")

        self._position = np.array(position, dtype=np.float32)
        if self._position.size != 3:
            raise ValueError("Position must be an 1d-numpy array [x y z].")

        self._normal = np.array([normal],  dtype=np.float32)
        if not (isinstance(self._normal, np.ndarray)) or self._normal.size != 3:
            raise ValueError("Normal must be an 1d-numpy array [x y z] dtype= float or int.")        

        self._mlambert = np.float32(mlambert)
        if self._mlambert.size > 1:
            raise ValueError("Lambert number must be scalar float.")
        elif mlambert <= 0:
            raise ValueError("Lambert number must be greater than zero.")        

        self._wavelengths = np.array(wavelengths, dtype=np.float32)
        if self._wavelengths.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of wavelengths array must be equal to the number of LEDs.")
        elif (np.any(self._wavelengths > 780) or np.any(self._wavelengths < 380)):
            raise ValueError(
                "Wavelengths must be between 380nm and 780 nm.")

        self._fwhm = np.array(fwhm, dtype=np.float32)
        if self._fwhm.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of FWHM array must be equal to the number of LEDs.")
        elif np.any(self._fwhm <= 0):
            raise ValueError(
                "FWDM must be non-negative.")


        if isinstance(constellation, np.ndarray):
            
            if len(constellation.shape) != 2:
                raise ValueError("Constellation must be a 2d-numpy array.")
            else:
                shape = constellation.shape
                if shape[0] != Kt.NO_LEDS:
                    raise ValueError("The number of rows must be equal to the number of LEDs.")
                elif np.ceil(np.log2(shape[1])) != np.floor(np.log2(shape[1])):
                    raise ValueError("The number of columns (number of symbols) must be power of 2")
                else:
                    self._constellation = constellation
                    self._order_csk = shape[1]          

        elif isinstance(constellation, str):

            if constellation == 'ieee16':
                self._constellation = Kt.IEEE_16CSK
                self._order_csk = 16
            elif constellation == 'ieee8':
                self._constellation = Kt.IEEE_8CSK
                self._order_csk = 8
            elif constellation == 'ieee4':
                self._constellation = Kt.IEEE_4CSK
                self._order_csk = 4
            else:
                raise ValueError("Constellation is not valid.")
        else:
            raise ValueError(
                """  
                Format of the constellation is not valid. String or np.array.
                Use list_csk() function from the Constant module or define correctly the 
                constellation symbols array (3xN numpy array).
                """
                )
            

        self._luminous_flux = np.float32(luminous_flux)        
        if self._luminous_flux <= 0:
            raise ValueError("The luminous flux must be non-negative.")

        # Initial functions
        self._init_function()

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
        self._position = np.array(position,  dtype=np.float32)
        if self._position.size != 3:
            raise ValueError("Position must be a 3d-numpy array.")
        self._init_function()

    @property
    def normal(self) -> np.ndarray:
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = np.array(normal,  dtype=np.float32)
        if self._normal.size != 3:
            raise ValueError("Normal must be a 3d-numpy array.")
        self._init_function()

    @property
    def mlambert(self) -> float:
        return self._mlambert

    @mlambert.setter
    def mlambert(self, mlabert):
        if mlabert <= 0:
            raise ValueError("Lambert number must be greater than zero.")
        self._mlambert = mlabert
        self._init_function()

    @property
    def wavelengths(self) -> np.ndarray:
        return self._wavelengths

    @wavelengths.setter
    def wavelengths(self, wavelengths):
        self._wavelengths = np.array(wavelengths,  dtype=np.float32)
        if self._wavelengths.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of wavelengths array must be equal to the number of LEDs.")
        self._init_function()

    @property
    def fwhm(self) -> np.ndarray:
        return self._fwhm

    @fwhm.setter
    def fwhm(self, fwhm):
        self._fwhm = np.array(fwhm,  dtype=np.float32)
        if self._fwhm.size != Kt.NO_LEDS:
            raise ValueError(
                "Dimension of FWHM array must be equal to the number of LEDs.") 
        self._init_function()

    @property
    def constellation(self) -> str:
        return self._constellation

    @constellation.setter
    def constellation(self, constellation):
        if isinstance(constellation, np.ndarray):
            
            if len(constellation.shape) != 2:
                raise ValueError("Constellation must be a 2d-numpy array.")
            else:
                shape =  constellation.shape
                if shape[0] != Kt.NO_LEDS:
                    raise ValueError("The number of rows must be equal to the number of LEDs.")
                elif np.ceil(np.log2(shape[1])) != np.floor(np.log2(shape[1])):
                    raise ValueError("The number of columns (number of symbols) must be power of 2")
                else:
                    self._constellation =  constellation
                    self._order_csk = shape[1]          

        elif isinstance(constellation, str):

            if constellation == 'ieee16':
                self._constellation = Kt.IEEE_16CSK
                self._order_csk = 16
            elif constellation == 'ieee8':
                self._constellation = Kt.IEEE_8CSK
                self._order_csk = 8
            elif constellation == 'ieee4':
                self._constellation = Kt.IEEE_4CSK
                self._order_csk = 4
            else:
                raise ValueError("Constellation is not valid.")
        else:
            raise ValueError(
                """  
                Format of the constellation is not valid. String or np.array.
                Use list_csk() function from the Constant module or define correctly the 
                constellation symbols array (3xN numpy array).
                """
                )
        self._init_function()

    @property
    def luminous_flux(self) -> float:
        return self._luminous_flux

    @luminous_flux.setter
    def luminous_flux(self, luminous_flux):
        if luminous_flux < 0:
            raise ValueError("The luminous flux must be non-negative.")
        self._luminous_flux = luminous_flux
        self._init_function()

    def __str__(self) -> str:
        return (
            f'\n List of parameters for LED transmitter: \n'
            f'Name: {self._name}\n'
            f'Position [x y z]: {self._position} \n'
            f'Normal Vector [x y z]: {self._normal} \n'
            f'Lambert Number: {self._mlambert} \n'            
            f'Central Wavelengths [nm]: {self._wavelengths} \n'
            f'FWHM [nm]: {self._fwhm}\n'
            f'Luminous Flux [lm]: {self._luminous_flux}\n'
            f'Correlated Color Temperature: {self._cct}\n'
            f'CIExy coordinates: {self._xyz}\n'                        
            f'ILER [W/lm]: \n {self._iler_matrix} \n'
            f'Average Power per Channel Color: \n {self._avg_power} \n'
            f'Total Power emmited by the Transmitter [W]: \n {self._total_power} \n'
        )   
    
    def _init_function(self) -> None:
        """
        Funtion to run the initial funtions to define the transmitter parameters
        """
        # Initial functions
        self._create_led_spd()        
        self._compute_iler(self._led_spd)
        self._avg_power_color()
        self._compute_cct()

    def plot_spatial_distribution(self) -> None:
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

        plt.title("Spatial Power Disstribution of the LED")
        plt.show()

    def plot_spatial_distibution_planec0_c180(self) -> None:

        # Define the angular range for PHI (C0-C360)
        phi = np.linspace(-np.pi/2, np.pi/2, 360)  # C0 to C360 in radians (0 to 2 * pi)

        # Calculate the LED spatial distribution based on the Lambertian model
        R = (self._mlambert + 1) / (2 * np.pi) * np.cos(phi) ** self._mlambert

        # Normalize the intensity (R values) by dividing by the maximum value
        R_normalized = R / np.max(R)

        # Rotate by 180 degrees by shifting phi
        phi_rotated = phi + np.pi

        # Plot the distribution in polar coordinates
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(phi_rotated, R_normalized, label=f'Lambertian order: {self._mlambert}')
        ax.set_title('LED Spatial Distribution (Rotated by 180°)')

        # Customizing the plot
        ax.set_theta_zero_location('N')  # Zero angle at the top (C0 direction)
        ax.set_theta_direction(-1)  # Clockwise direction
        ax.set_thetagrids(angles=np.arange(0, 360, 10))  # Add more polar grid angles

        plt.legend()
        plt.show()

    def _create_led_spd(self):
        """
        This function creates the normilized spectrum of the LEDs 
        from central wavelengths and FWHM.
        """
        # Array for wavelenght points from 380nm to (782-2)nm with 1nm steps
        self._array_wavelenghts = np.linspace(380, 780, Kt.SIZE_ARRAY_WAVELENGTHS)
        
        # Numpy Array to save the spectral power distribution of each color channel
        self._led_spd = np.zeros((self._array_wavelenghts.size, Kt.NO_LEDS))
        self._spd_normalized = np.zeros((self._array_wavelenghts.size, Kt.NO_LEDS))

        if self._led_type == 'gaussian':                     
            for i in range(Kt.NO_LEDS):
                # Arrays to estimates the normalized spectrum of LEDs
                self._led_spd[:, i] = self._gaussian_sprectrum(
                    self._array_wavelenghts,
                    self._wavelengths[i],
                    self._fwhm[i]/2
                    )                
                self._spd_normalized[:, i] = self._led_spd[:, i]/np.max(self._led_spd[:, i])
        elif self._led_type == 'custom':
            self._led_spd = self._rgb_led_spectrum[:, 1:]

            for i in range(Kt.NO_LEDS):
                self._spd_normalized[:, i] = self._led_spd[:, i]/np.max(self._led_spd[:, i])


    def plot_spd_at_1lm(self):
        """
        This funcion plots the spectral power distribution of the light source 
        at 1 lm in each channel.
        """
        # plot red spd data
        for i in range(Kt.NO_LEDS):
            plt.plot(self._array_wavelenghts, self._avg_power[i]*self._led_spd[:, i])
        
        plt.title("Spectral Power Distribution at 1 Lumen/Channel")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Power [W]")
        plt.grid()
        plt.show()
    
    def plot_spd_normalized(self):
        """
        This funcion plots the normalized spectral power distribution of the light source.
        """
        # plot red spd data
        for i in range(Kt.NO_LEDS):
            plt.plot(
                self._array_wavelenghts,
                self._spd_normalized[:, i]
                )
        
        plt.title("Normalized Spectral Power Distribution")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Normalized Power")
        plt.grid()
        plt.show()
    
    
    def _compute_iler(self, spd_data) -> None:        
        """
        This function computes the inverse luminous efficacy radiation (LER) matrix.
        This matrix has a size of NO_LEDS x NO_LEDS
        """
        self._photometric = lx.spd_to_power(
            np.vstack(
                    [
                        self._array_wavelenghts,
                        spd_data[:, 0]
                    ]),
            'pu'
        )
        self._radiometric = lx.spd_to_power(
            np.vstack(
                    [
                        self._array_wavelenghts,
                        spd_data[:, 0]
                    ]),
            'ru'
        )
        self._iler_matrix = np.zeros((Kt.NO_LEDS, Kt.NO_LEDS))
        self._iler_vector = np.zeros((Kt.NO_LEDS))

        for i in range(Kt.NO_LEDS):
            self._iler_matrix[i, i] = 1/lx.spd_to_ler(
                np.vstack(
                    [
                        self._array_wavelenghts,
                        spd_data[:, i]
                    ])
                )
            self._iler_vector[i] = self._iler_matrix[i, i]

    def _avg_power_color(self) -> None:
        """
        This function computes the average radiometric power emmitted by 
        each color channel in the defined constellation.
        """
        
        self._avg_lm = np.mean(
                    self._constellation,
                    axis=1
                    )
        self._avg_power = self._luminous_flux*np.transpose(
            np.matmul(
                self._iler_matrix,
                self._avg_lm
                )
            )

        self._total_power = np.sum(self._avg_power)
        # Manual setted of avg_power by each color channels
        #self._avg_power = np.array([1, 1, 1])

    def _compute_cct(self) -> None:
        """ 
        This function computes the CCT of the average radiated power by 
        the light source.            
        """
        # Computing the xyz coordinates from SPD-RGBY estimated spectrum
        self._XYZ_uppper = lx.spd_to_xyz(
            [
                self._array_wavelenghts,
                np.sum(self._avg_power*self._led_spd, axis=1)
            ])

        self._xyz = self._XYZ_uppper/np.sum(self._XYZ_uppper)

        # Computing the CCT coordinates from SPD-RGBY estimated spectrum
        self._cct = lx.xyz_to_cct_ohno2014(self._xyz)

    def _gaussian_sprectrum(self, x, mean, std) -> np.ndarray:
        """ This function computes a normal SPD of a monochromatic LED. """
        return (1 / (std * np.sqrt(2*np.pi))) * np.exp(-((x-mean)**2) / (2*std**2))