# annotating a variable with a type-hint
from typing import List, Tuple
#Numeric Numpy library
import numpy as np 
#Library for gaussian shape SPD
from scipy import stats
#Library to plot the LED patter, SPD and responsivity
import matplotlib.pyplot as plt
# import the required library
import torch
#import Luxpy library for colorimetric parameters
import luxpy as lx

#Import Constants Module
from vlc_rm.constants import Constants
#Import Constants Transmitter
from vlc_rm.transmitter import Transmitter
#Import Constants Photodetector
from vlc_rm.photodetector import Photodetector
#Import Constants Photodetector
from vlc_rm.indoorenv import Indoorenv



#Created a class objects 
Constants = Constants()


#Class for Recursive Model computations
class Recursivemodel:
    """ This class contains the function to calculates the CIR and DC-gain in the optical channel. """      

    # The init method or constructor
    def __init__(self, 
        name: str,
        led: Transmitter, 
        photodetector: Photodetector, 
        room: Indoorenv) -> None:
           
        # Instance Variable
        self.name = name
        self.led = led
        self.photodector = photodetector
        self.room = room      

        self._rgby_dcgain = np.zeros((1,Constants.NO_LEDS))
        self.channelmatrix = np.zeros((Constants.NO_DETECTORS,Constants.NO_LEDS),dtype=np.float32)         
        self._illuminance = 0
        self._cri = 0
        self._cct = 0
    
    #RGBY DC-Gain Property    
    @property
    def rgby_dcgain(self):
        """The RGBY DC-Gain property"""        
        return self._rgby_dcgain

    @rgby_dcgain.setter
    def rgby_dcgain(self,value):        
        self._rgby_dcgain =  value

    #Channel Matrix Property    
    @property
    def channelmatrix(self):
        """The Channel Matrix property"""        
        return self._channelmatrix
    
    @channelmatrix.setter
    def channelmatrix(self,value):        
        self._channelmatrix =  value

    #Illuminance Property    
    @property
    def illuminance(self):
        """The Channel Matrix property"""        
        return self._illuminance

    @illuminance.setter
    def illuminance(self,value):        
        self._illuminance =  value

    #CRI Property    
    @property
    def cri(self):
        """The Channel Matrix property"""        
        return self._cri

    @cri.setter
    def cri(self,value):        
        self._cri =  value

    #CCT Property    
    @property
    def cct(self):
        """The Channel Matrix property"""        
        return self._cct

    @cct.setter
    def cct(self,value):        
        self._cct =  value

    def __str__(self) -> str:
        return (
            f'Recursive model characteristics metrics: \n'
            f'DC-Gain [w]: {self._rgby_dcgain} \n'
            f'Crosstalk Matrix: \n{self._channelmatrix} \n' 
            f'Illuminance [lx]: {self._illuminance} \n'
            f'CCT: {self._cct} \n'
            f'CRI: {self._cri} \n'
        )

    # This method simulates the indoor enviornment
    def simulate_channel(self) -> None:
        
        self._compute_cir()
        self._compute_dcgain()
        self._create_spd()
        self._compute_cct_cri()
        self._compute_irradiance()
        self._compute_illuminance()
        self._compute_channelmatrix()

        print("|>>------- Indoor channel simulated ------<<|")       
        
    #Function to compute the CIR
    def _compute_cir(self) -> None:        
        """ Function to compute the channel impulse response for each reflection. 
    
        Parameters:
            led.m: lambertian number to tx emission                         
            led.wall_parameters: 3D array with distance and cosine pairwise-elemets.              
            pd.area: sensitive area in photodetector
            

        Returns: A list with 2d-array [power_ray,time_delay] collection for each 
        refletion [h_0,h_1,...,h_k].
        

        """       
        
        #defing variables and arrays
        tx_index_point = self.room.no_points-2                
        rx_index_point = self.room.no_points-1                
        
        cos_phi = np.zeros((self.room.no_points),dtype=np.float16)
        dis2 = np.zeros((self.room.no_points,self.room.no_points),dtype=np.float16)

        h0_se = np.zeros((self.room.no_points,4),dtype=np.float64)
        h0_er = np.zeros((self.room.no_points,1),dtype=np.float64)                  
                
       
        #Time delay between source and each cells 
        #h0_se[:,1] = room.wall_parameters[0,tx_index_point,:]/SPEED_OF_LIGHT
        #Time delay between receiver and each cells 
        #h0_er[:,1] = room.wall_parameters[0,rx_index_point,:]/SPEED_OF_LIGHT

        #define distance^2 and cos_phi arrays
        dis2 = np.power(self.room.wall_parameters[0,:,:],2)            
        cos_phi = self.room.wall_parameters[1,int(tx_index_point),:]
        #print("COS_PHI for Tx->",cos_phi)
        

        tx_power = (self.led.mlambert+1)/(2*np.pi)*np.multiply(np.divide(1,dis2[tx_index_point,:],out=np.zeros((self.room.no_points)), where=dis2[tx_index_point,:]!=0),np.power(cos_phi,self.led.mlambert))
        rx_wall_factor = self.photodector.area*self.room.wall_parameters[1,int(rx_index_point),:]

        #Differential power between all grid points without reflectance
        dP_ij = np.zeros((self.room.no_points,self.room.no_points),np.float32)
        dP_ij = np.divide(self.room.deltaA*self.room.wall_parameters[1,:,:]*np.transpose(self.room.wall_parameters[1,:,:]),np.pi*dis2,out=np.zeros_like(dP_ij),where=dis2!=0)         
        #print("Differential Power of Points->",dP_ij)
        
        
        #Array creation for dc_gain and previuos dc_gain
        self.h_k = []
        hlast_er = []
        
        #Array creation for time delay
        self.delay_hk = []
        delay_hlast_er = []

        #Time delay matrix
        tDelay_ij = np.zeros((self.room.no_points,self.room.no_points),dtype=np.float32)
        tDelay_ij = self.room.wall_parameters[0,:,:]/Constants.SPEED_OF_LIGHT
        #print(np.shape(tDelay_ij))


        for i in range(self.room.no_reflections+1):
            
            #Creates the array to save h_k reflections response and last h_er response
            self.h_k.append(np.zeros((self.room.no_points,4),np.float32))
            hlast_er.append(np.zeros((self.room.no_points,4),np.float32)) 

            #Creates the array to save time-delay reflections response and last h_er
            self.delay_hk.append(np.zeros((self.room.no_points,1),np.float32))
            delay_hlast_er.append(np.zeros((self.room.no_points,1),np.float32)) 


            if i == 0:           
                
                #Magnitude of CIR in LoS
                self.h_k[i][0,:] = tx_power[int(rx_index_point)]*rx_wall_factor[int(tx_index_point)]
                
                #Time Delay of CIR in LoS
                self.delay_hk[i][0,0] = tDelay_ij[int(tx_index_point),int(rx_index_point)]
                #print("self.delay_hk->",self.delay_hk[i][0,0])

                print("|>>--------------h{}-computed--------------<<|".format(i))              
                #numpy.savetxt(CIR_PATH+"h0.csv", h_k[i], delimiter=",")
                #print(self.h_k[i])

            elif i==1:

                
                #hlast_er[i] = np.multiply(np.reshape(h0_er[:,0],(-1,1)),self.room.reflectance_vectors)               
                
                #Impulse response between source and each cells without reflectance. The reflectance is added in the h_k computing.
                h0_se = np.multiply(np.reshape(np.multiply(self.room.deltaA*tx_power,self.room.wall_parameters[1,:,int(tx_index_point)]),(-1,1)),self.room.reflectance_vectors)

                #Impulse response between receiver and each cells 
                h0_er[:,0] = np.divide(np.multiply(self.room.wall_parameters[1,:,int(rx_index_point)],rx_wall_factor),np.pi*dis2[rx_index_point,:],out=np.zeros((self.room.no_points)), where=dis2[rx_index_point,:]!=0)
                
                #print("h0_se array->:",h0_se[:,0])
                #print("h0_er array->:",h0_er[:,0])       
                
                #Previous h_er RGBY vectors of magnitude for LoS
                hlast_er[i] = np.repeat(h0_er,repeats=4,axis=1)

                #Current vector for h1 impulse response for RGBY
                #Red-Green-Blue-Yellow                
                self.h_k[i] = np.multiply(h0_se,hlast_er[i])

                #Time-Delay computing
                delay_hlast_er[i] = tDelay_ij[int(rx_index_point),:]
                self.delay_hk[i] = tDelay_ij[int(tx_index_point),:] + delay_hlast_er[i]

                print("|>>--------------h{}-computed--------------<<|".format(i))              
                #np.savetxt(CIR_PATH+"h1.csv", h_k[i], delimiter=","              
                

            elif i>=2:                

                #Time-Delay computing
                delay_hlast_er[i] = np.sum(np.reshape(delay_hlast_er[i-1],(1,-1)) + tDelay_ij,axis=1)/self.room.no_points
                self.delay_hk[i] =  tDelay_ij[int(tx_index_point),:] + delay_hlast_er[i]

                #Computes the last h_er to compute h_k  
                #hlast_er[i] = np.multiply(hlast_er[i-1],np.multiply(self.room.reflectance_vectors,np.reshape(np.sum(dP_ij,axis=0),(-1,1))))
                for color in range(Constants.NO_LEDS):

                    hlast_er[i][:,color] = np.sum(np.multiply(hlast_er[i-1][:,color],np.multiply(self.room.reflectance_vectors[:,color],dP_ij)),axis=1)
                    #print("hlast->",np.shape(hlast_er[i]))

                    self.h_k[i][:,color] = np.multiply(h0_se[:,0],hlast_er[i][:,color])
                    #print("h_k->",np.shape(self.h_k[i]))                 


                


                print("|>>--------------h{}-computed--------------<<|".format(i))              
            
    #This function calculates the total power received from LoS and h_k reflections
    def _compute_dcgain(self) -> None:

        #print("\n Results DC Gain [R G B Y]:")          
        self.h_dcgain = np.zeros((self.room.no_reflections+1,4),np.float32)

        for i in range(0,self.room.no_reflections+1):
            self.h_dcgain[i,:] = np.sum(self.h_k[i][0:-2,0:4], axis = 0) 
            #print(" H"+str(i)+" RGBY DC Gain Power [W]:")          
            #print(self.h_dcgain[i,:])


        self._rgby_dcgain = np.sum(self.h_dcgain, axis = 0)
        #print("DC-gain channel computted")
        #print("Total RGBY DC Gain Power [W]")
        #print(self.rgby_dcgain)

    #Function to create histograms from channel impulse response raw data.
    def _create_histograms(self) -> None:
        """Function to create histograms from channel impulse response raw data. 
        
        The channel impulse response raw data is a list with power and time delay 
        of every ray. Many power histograms are created based on time resolution 
        defined in the TIME_RESOLUTION constant. 

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

        self.total_histogram = np.zeros((self.bins_hist,4))
        self.hist_power_time = []
        delay_aux = np.zeros((room.no_points,1))

        print("//------------- Data report ------------------//")
        print("Time resolution [s]:"+str(self.time_resolution))
        print("Number of Bins:"+str(self.bins_hist))      
        
        delay_los = self.delay_hk[0][0,0]        
        #print(np.shape(delay_los))        
        
        print("Optical power reported in histograms:")

        for k_reflec in range(self.room.no_reflections+1):            
            
            self.hist_power_time.append(np.zeros((self.bins_hist,4),np.float32))      

            #Delay_aux variable
            delay_aux = np.reshape(self.delay_hk[k_reflec],(-1,1)) - delay_los
            delay_aux = np.floor(delay_aux/self.time_resolution)
            #print(np.shape(delay_aux))

            for j in range(self.room.no_points):
                #print(int(delay_aux[j]))                
                #print(self.h_k[i][j,:])
                self.hist_power_time[k_reflec][int(delay_aux[j,0]),:] += self.h_k[k_reflec][j,:]

                    
            self.time_scale = linspace(0,self.bins_hist*self.time_resolution,num=self.bins_hist)          
            print("H" + str(k_reflec) + ": " , np.sum(self.hist_power_time[k_reflec],axis=0))       

            self.total_histogram += self.hist_power_time[k_reflec]
        

    #This function plots the channel impulse response for 4 colors
    def _plot_cir(self,channel: str = "") -> None:
        
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
            print("Invalid color name ('red' or 'green' or 'blue' or 'yellow').")
            color_number = -1        

        if color_number == -1:
            print("Graphs were not generated.")
        else:
            for k_reflec in range(0,room.no_reflections+1):            
                     
                fig, (vax) = plt.subplots(1, 1, figsize=(12, 6))
                
                vax.plot(self.time_scale,self.hist_power_time[k_reflec][:,color_number], 'o',markersize=2)
                vax.vlines(self.time_scale,[0],self.hist_power_time[k_reflec][:,color_number],linewidth=1)

                vax.set_xlabel("time(s) \n Time resolution:",fontsize=15)
                vax.set_ylabel('Power(W)',fontsize=15)
                vax.set_title("Channel "+self.channel+" Impulse Response h"+str(k_reflec)+"(t)",fontsize=20)

                vax.grid(color = 'black', linestyle = '--', linewidth = 0.5)
                
                
                fig.savefig(Constants.REPORT_PATH+"h"+str(k_reflec)+".png")        
                plt.show()


            fig, (vax) = plt.subplots(1, 1, figsize=(12, 6))
            
            vax.plot(self.time_scale,self.total_histogram[:,color_number], 'o',markersize=2)
            vax.vlines(self.time_scale,[0],self.total_histogram[:,color_number],linewidth=1)

            vax.set_xlabel("time(s) \n Time resolution:",fontsize=15)
            vax.set_ylabel('Power(W)',fontsize=15)
            vax.set_title("Channel "+self.channel+" Total Impulse Response h(t)",fontsize=20)

            vax.grid(color = 'black', linestyle = '--', linewidth = 0.5)
            
            
            fig.savefig(Constants.REPORT_PATH+self.channel+"-htotal.png")        
            plt.show()


    #This function creates a SPD of LED from central wavelengths, FWHM and DC gain of channel
    def _create_spd(self) -> None:        
        
        #Array for wavelenght points from 380nm to (782-2)nm with 2nm steps
        self.wavelenght = np.arange(380, 782, 2) 
        
        #Arrays to estimate the RGBY gain spectrum
        self.r_data = self.rgby_dcgain[0]*stats.norm.pdf(self.wavelenght, self.led._wavelengths[0], self.led._fwhm[0]/2)
        self.g_data = self.rgby_dcgain[1]*stats.norm.pdf(self.wavelenght, self.led._wavelengths[1], self.led._fwhm[1]/2)
        self.b_data = self.rgby_dcgain[2]*stats.norm.pdf(self.wavelenght, self.led._wavelengths[2], self.led._fwhm[2]/2)
        self.y_data = self.rgby_dcgain[3]*stats.norm.pdf(self.wavelenght, self.led._wavelengths[3], self.led._fwhm[3]/2)
        self.spd_data = [self.r_data , self.g_data , self.b_data , self.y_data]


    #This function plots the SPD of QLED
    def _plot_spd(self) -> None:

        ## plot red spd data
        plt.plot(self.wavelenght,self.r_data,'r')
        plt.plot(self.wavelenght,self.g_data,'g')
        plt.plot(self.wavelenght,self.b_data,'b')
        plt.plot(self.wavelenght,self.y_data,'y')
        plt.title("Spectral Power distribution of QLED")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Radiometric Power [W]")
        plt.grid()
        plt.show()


    #This function calculates a CCT and CRI of the QLED SPD.
    def _compute_cct_cri(self) -> None:
        
        #Computing the xyz coordinates from SPD-RGBY estimated spectrum
        xyz = lx.spd_to_xyz([self.wavelenght,self.r_data + self.g_data + self.b_data + self.y_data])
        #Computing the CRI coordinates from SPD-RGBY estimated spectrum
        self._cri = lx.cri.spd_to_cri(np.vstack([self.wavelenght,(self.r_data + self.g_data + self.b_data + self.y_data)/self.photodector.area]))
        #Computing the CCT coordinates from SPD-RGBY estimated spectrum
        self._cct = lx.xyz_to_cct_ohno2014(xyz)       
        

    #This function calculates the irradiance.
    def _compute_irradiance(self) -> None:                
        
        self._irradiance = lx.spd_to_power(np.vstack([self.wavelenght,(self.r_data + self.g_data + self.b_data + self.y_data)/self.photodector.area]),ptype = 'ru')        


    #This function calculates the illuminance.
    def _compute_illuminance(self) -> None:
        
        self._illuminance = lx.spd_to_power(np.vstack([self.wavelenght,(self.r_data + self.g_data + self.b_data + self.y_data)/self.photodector.area]),ptype = 'pu')         


    #This function computes channel matrix
    def _compute_channelmatrix(self) -> None:      
        
        
        #print(self.wavelenght)
        #print(self.responsivity[:,0])

        for j in range(0,Constants.NO_LEDS):
            for i in range(1,Constants.NO_DETECTORS+1):
                #print(self.spd_data[j])
                #print(self.responsivity[:,i])
                #print(i,'-',j)
                self._channelmatrix[i-1][j] = np.dot(self.spd_data[j],self.photodector.responsivity[:,i])     
                
