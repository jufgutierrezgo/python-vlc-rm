import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Transmitter
from vlc_rm.transmitter import Transmitter
# Import Photodetector
from vlc_rm.photodetector import Photodetector
# Import Symbol Constants
from vlc_rm.constants import Constants as Kt

import matplotlib.pyplot as plt

import numpy as np

from numpy import loadtxt

# test to create a SER curves of an indoor enviornment
def test_ser_curves():    

    # load the spectral reflectance of Plaster material
    ser_p1 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD1.txt"
        )
    ser_p2 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD2.txt"
        )
    ser_p3 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD3.txt"
        )
    ser_p4 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD4.txt"
        )
    ser_p5 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD5.txt"
        )
    ser_p6 = loadtxt(
        "tests/ser_flux_curves/SER-Flux_dataPD6.txt"
        )
    print(ser_p1)
        
    plt.plot(
            ser_p1[0, :],
            ser_p1[1, :],
            color='black',
            linestyle='solid',
            label='Position P1',
            marker='+',
            markersize=10
        )    
    plt.plot(
            ser_p2[0, :],
            ser_p2[1, :],
            color='black',
            linestyle='dotted',
            label='Position P2',
            marker='o',
            markersize=10
        )    
    plt.plot(
            ser_p3[0, :],
            ser_p3[1, :],
            color='black',
            linestyle='dashed',
            label='Position P3',
            marker='x',
            markersize=10
        )     
    #plt.title("Spectral Response of LEDs and Detectors", fontsize=20)
    plt.legend(
        loc='upper right',
        fontsize=16,
        ncol=1,
        # bbox_to_anchor=[0, 1],
        # shadow=True, 
        # fancybox=True
        )
    plt.xticks(
        # rotation=90,
        fontsize=18
        )
    plt.yticks(
        # rotation=90,
        fontsize=18
        )        
    # convert y-axis to Logarithmic scale
    plt.yscale("log")    
    # plt.title()
    plt.xlabel("Luminous Flux [lm]", fontsize=20)
    plt.ylabel("Symbol Error Rate", fontsize=20)
    plt.grid()
    plt.show()

