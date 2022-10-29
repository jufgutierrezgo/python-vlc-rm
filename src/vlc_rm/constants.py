import os


#Class constants
class Constants:
    # global variables

    #Array with normal vectors for each wall.
    NORMAL_VECTOR_WALL = [[0,0,-1],[0,1,0],[1,0,0],[0,-1,0],[-1,0,0],[0,0,1]]
    #directory root of the project
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #directory to save channel impulse response raw data
    SENSOR_PATH = ROOT_DIR + "/sensors/"
    #directory to save histograms and graphs  
    REPORT_PATH = ROOT_DIR + "/report/"
    #Numbers of LED (Transmission channels)
    NO_LEDS = 4
    #Numbers of Photodetector Channels
    NO_DETECTORS = 3
    #Speed of light
    SPEED_OF_LIGHT = 299792458

