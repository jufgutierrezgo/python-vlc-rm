# annotating a variable with a type-hint
from typing import List, Tuple
#Numeric Numpy library
import numpy as np 
#Library to plot the LED patter, SPD and responsivity
import matplotlib.pyplot as plt
#Import Constants Modules
from vlc_rm.constants import Constants

#Created a class objects 
Constants = Constants()

#Class for the photodetector
class Photodetector:    

    # The init method or constructor
    def __init__(self, 
        name: str, 
        position: Tuple[float,float,float], 
        normal: Tuple[float,float,float], 
        area: Tuple[float,float,float], 
        sensor: str ="", 
        fov: float =90) -> None:
           
        # Instance Variable
        self._name = name
        self._position = np.array(position)
        self._normal = np.array([normal])
        self._area = np.array(area)    
        self._fov = fov
        self._sensor = sensor 
    
        if self.sensor == 'TCS3103-04':            
            #read text file into NumPy array
            self.responsivity = np.loadtxt(Constants.SENSOR_PATH+"ResponsivityTCS3103-04.txt")
            print("Responsivity loaded succesfully")                       
        elif self.sensor == 'S10917-35GT':            
            #read text file into NumPy array
            self.responsivity = np.loadtxt(Constants.SENSOR_PATH+"ResponsivityS10917-35GT.txt")                       
            print("Responsivity loaded succesfully")
        elif self.sensor == '': 
            print("Specify sensor reference")
        else:
            print("Sensor reference not valid")  

    #Name Property    
    @property
    def name(self) -> str:
        """The name property"""    
        return self._name

    @name.setter
    def name(self,value):        
        self._name =  value

    #Position Property    
    @property
    def position(self) -> Tuple[float,float,float]:
        """The position property"""
        return self._position

    @position.setter
    def position(self,position):        
        self._position =  position    

    #Normal Property
    @property
    def normal(self) -> Tuple[float,float,float]:
        """The normal property"""        
        return self._normal

    @normal.setter
    def position(self,normal):        
        self._normal = np.array(normal)        

    #Area Property    
    @property
    def area(self) -> float:
        """The position property"""        
        return self._area

    @area.setter
    def area(self,area):        
        self._area =  area

    #FOV Property    
    @property
    def fov(self)  -> float:
        """The position property"""
        return self._fov

    @fov.setter
    def fov(self,fov):        
        self._fov =  fov
    
    #Sensor Property    
    @property
    def sensor(self) -> str:
        """The position property"""
        return self._sensor

    @sensor.setter
    def sensor(self,sensor) -> None:
        self._sensor =  sensor

        if self.sensor == 'TCS3103-04':            
            #read text file into NumPy array
            self.responsivity = np.loadtxt(Constants.SENSOR_PATH+"ResponsivityTCS3103-04.txt")
            print("Responsivity loaded succesfully")                       
        elif self.sensor == 'S10917-35GT':            
            #read text file into NumPy array
            self.responsivity = np.loadtxt(Constants.SENSOR_PATH+"ResponsivityS10917-35GT.txt")                       
            print("Responsivity loaded succesfully")
        elif self.sensor == '': 
            print("Specify sensor reference")
        else:
            print("Sensor reference not valid")  
    
    def __str__(self) -> str:
        return (
            f'\nList of parameters for photodetector: \n'
            f'Position [x y z]: {self._position} \n'
            f'Normal Vector [x y z]: {self._normal} \n'
            f'Active Area[m2]: {self._area} \n'
            f'FOV: {self._fov} \n'        
            f'Sensor: {self._sensor}'            
        )

    # Plot the spectral responsivity of the photodetector.
    def plot_responsivity(self) -> None:
        plt.plot(self.responsivity[:,0],self.responsivity[:,1],color='r', linestyle='dashed') 
        plt.plot(self.responsivity[:,0],self.responsivity[:,2],color='g', linestyle='dashed') 
        plt.plot(self.responsivity[:,0],self.responsivity[:,3],color='b', linestyle='dashed')
        plt.title("Spectral Responsiity of Photodetector")
        plt.xlabel("Wavelength [nm]")
        plt.ylabel("Responsivity [A/W]")
        plt.grid()
        plt.show()

